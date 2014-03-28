import logging
logger = logging.getLogger("debugging")

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from siteup_api.models import *
from siteup_api import validators

class CheckGroupTestCase(TestCase):
    def setUp(self):
        u = User.objects.create_user(
            username='TestUser',
            email='test@user.com',
            password='1234'
        )

        self.g = CheckGroup.objects.create(
            title="Test Group",
            owner = u
        )

        self.d1 = DnsCheck.objects.create(
            title='DNS Test 1',
            group=self.g,
            target='josetomastocino.com',
            record_type='A',
            resolved_address='78.47.140.228'
        )

        self.d2 = DnsCheck.objects.create(
            title='DNS Test 1',
            group=self.g,
            target='josetomastocino.com',
            record_type='A',
            resolved_address='1.1.1.1'
        )

    def test_get_checks(self):
        checks = self.g.checks()

        self.assertEqual(len(checks), 2)

    def test_activation(self):
        self.g.disable()
        self.assertTrue(all([x.is_active == False for x in self.g.checks()]))
        self.g.enable()
        self.assertTrue(all([x.is_active == True for x in self.g.checks()]))


