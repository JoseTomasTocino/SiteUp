from celery.task.schedules import crontab
from celery.decorators import periodic_task

from siteup.celery import app
from siteup_api import models

from time import sleep
from random import randrange

@app.task
def nap(t):
    sleep(t)
    print "Slept for %i seconds" % t


# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def test():
    kk = models.PingCheck.objects.all()
    print "lol wut", kk
    numtasks = randrange(4,8)
    for f in range(numtasks):
        nap.delay(randrange(6))

    print "Enqueued %i tasks" % numtasks


"""

Launch celery beat using:

    celery beat -A siteup -l info

And the worker using:

    celery worker -A siteup -l info

You can do it all in one single step using

    celery worker -B -A siteup -l info

More processes can be launched in a worker using -c 16
"""


