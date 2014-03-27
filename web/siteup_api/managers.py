import datetime

from django.db import models
from django.db.models import Q

class CheckLogManager(models.Manager):

    def last_24_hours(self, *args, **kwargs):
        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(hours=24))

    def last_week(self, *args, **kwargs):
        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7), date__lt=datetime.datetime.now() - datetime.timedelta(hours=24))

    @staticmethod
    def _with_extra (q):

        # Just use the logs with valid status OR those with a response_time > 0
        # thus avoiding having a min. response time of 0 when pings could not be completed

        q_ok = q.filter(Q(status=0) | Q(response_time__gt=0))
        q_len = float(len(q_ok))

        # Avoid division by zero
        if q_len == 0:
            return {
                'objs' : q,
                'avg_response_time': '',
                'avg_status': '',
                'max_response_time': '',
                'min_response_time': ''
            }

        resp_times = [int(x.response_time) for x in q_ok]
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
