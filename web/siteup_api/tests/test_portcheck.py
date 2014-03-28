import logging
logger = logging.getLogger("debugging")

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from siteup_api.models import *
from siteup_api import validators

class PortTestCase(TestCase):
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

        self.d1 = PortCheck.objects.create(
            title='Port Test 1',
            group=g,
            target='josetomastocino.com',
            target_port=80,
        )

        self.d2 = PortCheck.objects.create(
            title='Port Test 1',
            group=g,
            target='ftp.mozilla.org',
            target_port=21,
            response_check_string='Mozilla',
        )

        # self.d3 = PortCheck.objects.create(
        #     title='Port Test 2',
        #     group=g,
        #     target='josetomastocino.com',
        #     record_type='A',
        #     resolved_address='1.1.1.1'
        # )

    def test_port_ok(self):
        self.d1.run_check()
        check_log = self.d1.logs.get()
        self.assertEqual(check_log.status, 0)

    def test_port_and_content_ok(self):
        self.d2.run_check()
        check_log = self.d2.logs.get()
        self.assertEqual(check_log.status, 0)

    # def test_dns_down_check(self):
    #     self.d2.run_check()
    #     check_log = self.d2.logs.get()
    #     self.assertEqual(check_log.status, 1)