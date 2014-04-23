import logging
logger = logging.getLogger("debugging")

from django.conf import settings
from django.test import TestCase

from siteup_api.models import *
from siteup_checker import tasks

from datetime import datetime, timedelta

class TestRemoveOldLogs(TestCase):

    def setUp(self):
        u = User.objects.create_user(
            username='TestUser',
            email='test@user.com',
            password='1234'
        )

        g = CheckGroup.objects.create(
            title="Test Group",
            owner = u
        )

        self.d1 = DnsCheck.objects.create(
            title='DNS Test 1',
            group=g,
            target='josetomastocino.com',
            record_type='A',
            resolved_address='78.47.140.228'
        )

        c1 = CheckLog()
        c1.check = self.d1
        c1.save(update_check = False)

        # Need to do it this way to override auto_now_add behavior
        c1.date = datetime.now() - settings.CHECKLOG_EXPIRATION_TIME - timedelta(hours=1)
        c1.save(update_check = False)

        c1 = CheckLog()
        c1.check = self.d1
        c1.save(update_check = False)
        logger.info(c1.date)


    def test_removal(self):
        self.assertEqual(len(self.d1.logs.all()), 2)
        tasks.remove_old_logs()
        self.assertEqual(len(self.d1.logs.all()), 1)