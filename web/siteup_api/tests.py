import logging
logger = logging.getLogger(__name__)

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from siteup_api.models import *
from siteup_api import validators
from siteup_checker import monitoring

class DnsTestCase(TestCase):
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

        self.d2 = DnsCheck.objects.create(
            title='DNS Test 1',
            group=g,
            target='josetomastocino.com',
            record_type='A',
            resolved_address='1.1.1.1'
        )

    def test_dns_ok_check(self):
        self.d1.run_check()
        check_log = DnsCheckLog.objects.get(check=self.d1)
        self.assertTrue(check_log.is_ok)

    def test_dns_not_ok_check(self):
        self.d2.run_check()
        check_log = DnsCheckLog.objects.get(check=self.d2)
        self.assertFalse(check_log.is_ok)


class HttpTestCase(TestCase):
    def setUp(self):

        u = User.objects.create_user(
          username='TestUser',
          email='test@user.com',
          password='1234')

        g = CheckGroup.objects.create(
          title="Test Group",
          owner = u)

        self.h1 = HttpCheck.objects.create(title='HTTP Test 1',
                                          group=g,
                                          target='http://josetomastocino.com')

        self.h2 = HttpCheck.objects.create(title='HTTP Test 2',
                                          group=g,
                                          target='http://josetomastocino.com',
                                          content_check_string='Ingeniero')

    def test_http_ok_check(self):
        self.h1.run_check()
        check_log = HttpCheckLog.objects.get(check=self.h1)
        self.assertTrue(check_log.is_ok)

    def test_http_not_ok_check(self):
        self.h2.run_check()
        check_log = HttpCheckLog.objects.get(check=self.h2)
        print check_log.value
        self.assertTrue(check_log.is_ok)


class ValidatorsTestCase(TestCase):
    def test_validate_hostname(self):
        try:
            validators.validate_hostname('josetomastocino.com')
        except ValidationError:
            self.fail('validators.validate_hostname failed')

        with self.assertRaises(ValidationError):
            validators.validate_hostname('josetomastocino com')

    def test_validate_ip_or_hostname(self):
        try:
            validators.validate_ip_or_hostname('josetomastocino.com')
            validators.validate_ip_or_hostname('192.168.1.1')
        except ValidationError:
            self.fail('validators.validate_ip_or_hostname failed')

        with self.assertRaises(ValidationError):
            validators.validate_ip_or_hostname('Lorem ipsum dillum sit amet')


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



# logger.error("LOLWAT")

# print monitoring.check_ping('localhost')
# print monitoring.check_dns('josetomastocino.com', 'A', '78.47.140.228')
# print monitoring.check_http_header('http://josetomastocino.com/', 200)
# print monitoring.check_http_content('http://josetomastocino.com', 'Ingeniero')


# class PingTestCase(TestCase):
#     def setup(self):
#         u = User.objects.create_user(username='TestUser', email='test@user.com', password='1234')
#         self.d1 = PingCheck(title='Ping Test 1',
#                             owner=u,
#                             target='josetomastocino.com')
#
#     def test_ping_check(self):
#         pass


# Create your tests here.
