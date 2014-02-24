import logging
logger = logging.getLogger(__name__)

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from siteup.celery import app
from siteup_api import models

from time import sleep
from random import randrange

import datetime

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

    logger.info("Enqueued %i checks" % len(active_checks))

@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def remove_old_logs():
    date_limit = datetime.datetime.now() - datetime.timedelta(hours=settings.CHECKLOG_EXPIRATION_TIME)
    checks = models.CheckLog.objects.filter(date__lt=date_limit)
    logger.info("Deleting %i old check logs..." % len(checks))
    checks.delete()


"""

Launch celery beat using:

    celery beat -A siteup -l info

And the worker using:

    celery worker -A siteup -l info

You can do it all in one single step using

    celery worker -B -A siteup -l info

More processes can be launched in a worker using -c 16
"""


