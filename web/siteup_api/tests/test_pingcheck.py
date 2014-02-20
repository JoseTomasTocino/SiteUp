import logging
logger = logging.getLogger(__name__)

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from siteup_api.models import *
from siteup_api import validators

class PingTestCase(TestCase):
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

        self.h1 = PingCheck.objects.create(
            title='Ping Test 1',
            group=g,
            target='josetomastocino.com'
        )

        self.h2 = PingCheck.objects.create(
            title='Ping Test 2',
            group=g,
            target='josetomastocino.com',
            should_check_timeout = True,
            timeout_value=1000,
        )


    def test_ping_up(self):
        self.h1.run_check()
        check_log = PingCheckLog.objects.get(check=self.h1)
        self.assertEqual(check_log.status, 0)

    def test_ping_up_within_timeout(self):
        self.h2.run_check()
        check_log = PingCheckLog.objects.get(check=self.h2)
        self.assertEqual(check_log.status, 0)