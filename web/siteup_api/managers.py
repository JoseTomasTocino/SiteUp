import datetime
import logging
logger = logging.getLogger("debugging")

from django.db import models
from django.db.models import Q

class CheckLogManager(models.Manager):

    def last_24_hours(self, *args, **kwargs):
        """
        Returns the CheckLogs created within the last 24 hours.
        """

        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(hours=24))

    def last_week(self, *args, **kwargs):
        """
        Returns the CheckLogs created the previous week (not including the present day).
        """

        return self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7), date__lt=datetime.datetime.now() - datetime.timedelta(hours=24))

    def last_24_hours_with_avg(self, *args, **kwargs):
        """
        Returns the CheckLogs created within the last 24 hours with some details averaged.
        """

        q = self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(hours=24))
        return CheckLogManager._with_extra(q)

    def last_week_with_avg(self, *args, **kwargs):
        """
        Returns the CheckLogs created the previous week (not including the present day) with some details averaged.
        """

        q = self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(days=7), date__lt=datetime.datetime.now() - datetime.timedelta(hours=24))
        return CheckLogManager._with_extra(q)

    def in_period(self, check_type, **kwargs):
        q = self.filter(date__gt=datetime.datetime.now() - datetime.timedelta(**kwargs))

        ret = CheckLogManager._with_extra(q)
        return ret



    @staticmethod
    def _with_extra (q):
        """
        Computes and returns the average, min and max response time within the received CheckLog QuerySet.
        """

        # Compute average uptime (with all logs)
        avg_status = int(sum((int(x.status == 0) for x in q)) / float(len(q)) * 100)

        # To calculate the other stats, just use the logs with valid status OR
        # those with a response_time > 0 thus avoiding having a min. response
        # time of 0 when pings could not be completed and other similar situations

        q_ok = q.filter(Q(status=0) | Q(response_time__gt=0))
        q_len = float(len(q_ok))

        # Return empty values if there are no good logs
        if q_len == 0:
            return {
                'objs' : q,
                'avg_status': avg_status,
                'avg_response_time': '',
                'max_response_time': '',
                'min_response_time': ''
            }


        # Isolate response times
        resp_times = [int(x.response_time) for x in q_ok]

        # Compute average response time
        avg_response_time = sum(resp_times) / q_len

        return {
            'objs' : q,
            'avg_status': avg_status,
            'avg_response_time': avg_response_time,
            'max_response_time': max(resp_times),
            'min_response_time': min(resp_times)
        }


