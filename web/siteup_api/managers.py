import datetime

from django.db import models

class CheckLogManager(models.Manager):

    def last_24_hours(self, *args, **kwargs):
        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(hours=24))