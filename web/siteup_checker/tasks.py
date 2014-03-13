import logging
logger = logging.getLogger(__name__)

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from siteup.celery import app
from siteup_api import models

from time import sleep
from random import randrange

import datetime
from itertools import groupby

from django.conf import settings

@app.task
def run_check(x):
    x.run_check()

def enqueue_check(x):
    run_check.delay(x)


# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def enqueue_checks():
    active_checks = []

    # Fetch active checks
    for check_type in models.CHECK_TYPES:
        active_checks.extend(check_type.objects.filter(is_active=True))

    # Enqueue checking for active checks
    for check in active_checks:
        enqueue_check(check)

    logger.info(u"Enqueued %i checks" % len(active_checks))


@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def remove_old_logs():

    # Calculate the limit date from which the checks will be deleted
    date_limit = datetime.datetime.now() - datetime.timedelta(hours=settings.CHECKLOG_EXPIRATION_TIME)

    # Get the CheckLogs older than the limit date
    checks = models.CheckLog.objects.filter(date__lt=date_limit)

    # Output to the logger
    logger.info(u"Deleting %i old check logs..." % len(checks))

    # Delete them niggas
    checks.delete()

    # Same as before, calculate the limit date
    date_limit = datetime.datetime.now() - datetime.timedelta(hours=settings.CHECKSTATUS_EXPIRATION_TIME)

    # Get the CheckStatus. Filter the active ones
    statuses = models.CheckStatus.objects.filter(date_start__lt=date_limit).exclude(date_end=None)

    # Log the action
    logger.info(u"Deleting %i old check statuses..." % len(statuses))

    statuses.delete()


@periodic_task(run_every=crontab(hour="*", minute="*/35", day_of_week="*"))
def collapse_logs():

    logger.info(u"Issued COLLAPSE_LOGS task")

    # Calcualte the limit date
    date_limit = datetime.datetime.now() - datetime.timedelta(hours=settings.CHECKLOG_COLLAPSE_TIME_1)

    # To group the logs by 30-min intervals, the group function checks the first digit of the minutes in the time
    get_interval = lambda l: l.date.isoformat()[:14] + ('0' if int(l.date.isoformat()[14]) < 3 else '3')

    # Go check by check
    for check_type in models.CHECK_TYPES:
        for check in check_type.objects.all():

            # Get uncollapsed, old enough logs
            uncollapsed_logs = check.logs.order_by('date').filter(collapse_level=0, date__lt=date_limit)

            if not uncollapsed_logs:
                continue

            logger.info("COLLAPSE - Check {} has {} logs to be collapsed".format(check.title, len(uncollapsed_logs)))

            # Get the first interval
            last_interval = None
            current_interval_start = None

            # Go through all logs
            for i, log in enumerate(uncollapsed_logs):

                # Calculate interval for current log
                current_interval = get_interval(log)

                # If still on the same interval, keep going
                if current_interval == last_interval:
                    continue

                # If intervals do not match but last interval was not initialized, continue as well
                elif not last_interval:
                    last_interval = current_interval
                    current_interval_start = i
                    # assert(i == 0)
                    continue

                last_interval = current_interval

                # If not, close the previous interval
                current_interval_end = i

                # Get the logs within the interval
                current_interval_logs = uncollapsed_logs[current_interval_start:current_interval_end]

                logger.info("New interval, from %s to %s" % (current_interval_logs[0].date, current_interval_logs[-1].date))

                # Just cache the base for the mean calculations
                avg_base = float(len(current_interval_logs))

                # Calculate the average status of the CheckLogs within the interval.
                mean_status = round(sum((1 if x.status in (1, 2) else 0 for x in current_interval_logs)) / avg_base)

                # Calculate the average response time. Does not make sense for anything else than PingCheck's logs, but still
                mean_response_time = round(sum((x.response_time for x in current_interval_logs)) / avg_base)

                # Get the max response time in the interval
                max_response_time = max((x.response_time for x in current_interval_logs))

                # Build new time zeroing out the second digit of the minutes and the seconds
                new_date = datetime.datetime.strptime( current_interval + "0:00", "%Y-%m-%dT%H:%M:%S" )

                # Save the new information in the first CheckLog of the interval
                cl = current_interval_logs[0]
                cl.status = mean_status
                # cl.response_time = mean_response_time
                cl.response_time = max_response_time
                cl.date = new_date
                cl.collapse_level = 1
                cl.save(update_check=False)

                # Delete the rest of CheckLogs in the interval
                [x.delete() for x in current_interval_logs[1:]]

                #Reset the counter
                current_interval_start = i





"""

Launch celery beat using:

    celery beat -A siteup -l info

And the worker using:

    celery worker -A siteup -l info

You can do it all in one single step using

    celery worker -B -A siteup -l info

More processes can be launched in a worker using -c 16
"""


