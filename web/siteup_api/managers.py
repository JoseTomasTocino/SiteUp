import datetime

from django.db import models

class CheckLogManager(models.Manager):

    def last_24_hours(self, *args, **kwargs):
        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(hours=24))

    def last_week(self, *args, **kwargs):
        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7), date__lt=datetime.datetime.now() - datetime.timedelta(hours=24))