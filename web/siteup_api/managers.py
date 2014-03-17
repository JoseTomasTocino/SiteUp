import datetime

from django.db import models

class CheckLogManager(models.Manager):

    def last_24_hours(self, *args, **kwargs):
        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(hours=24))

    def last_week(self, *args, **kwargs):
        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7), date__lt=datetime.datetime.now() - datetime.timedelta(hours=24))

    @staticmethod
    def _with_extra (q):
        q_len = float(len(q))
        resp_times = [int(x.response_time) for x in q]
        avg_response_time = sum(resp_times) / q_len
        avg_status = int(sum((int(x.status == 0) for x in q)) / q_len * 100)

        return {
            'objs' : q,
            'avg_response_time': avg_response_time,
            'avg_status': avg_status,
            'max_response_time': max(resp_times),
            'min_response_time': min(resp_times)
        }

    def last_24_hours_with_avg(self, *args, **kwargs):
        q = self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(hours=24))
        return CheckLogManager._with_extra(q)

    def last_week_with_avg(self, *args, **kwargs):
        q = self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7), date__lt=datetime.datetime.now() - datetime.timedelta(hours=24))
        return CheckLogManager._with_extra(q)
