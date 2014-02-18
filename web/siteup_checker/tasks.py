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
    numtasks = randrange(2,6)
    for f in range(numtasks):
        nap.delay(randrange(5))

    print "Enqueued %i tasks" % numtasks




