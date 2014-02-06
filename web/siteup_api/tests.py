from django.test import TestCase
from django.contrib.auth.models import User

from siteup_api.models import DnsCheck, DnsCheckLog, PortCheck, HttpCheck, PingCheck


class DnsTestCase(TestCase):
    def setUp(self):
        u = User.objects.create_user(username='TestUser', email='test@user.com', password='1234')
        self.d1 = DnsCheck.objects.create(title='DNS Test 1',
                                          owner=u,
                                          target='josetomastocino.com',
                                          register_type='A',
                                          resolved_address='78.47.140.228')

        self.d2 = DnsCheck.objects.create(title='DNS Test 1',
                                          owner=u,
                                          target='josetomastocino.com',
                                          register_type='A',
                                          resolved_address='1.1.1.1')

    def test_dns_ok_check(self):
        self.d1.run_check()
        check_log = DnsCheckLog.objects.get(check=self.d1)
        self.assertTrue(check_log.is_ok)

    def test_dns_not_ok_check(self):
        self.d2.run_check()
        check_log = DnsCheckLog.objects.get(check=self.d2)
        self.assertFalse(check_log.is_ok)


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
