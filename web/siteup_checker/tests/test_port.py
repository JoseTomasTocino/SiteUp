import logging
logger = logging.getLogger(__name__)

from django.test import TestCase

from siteup_checker import monitoring

class TestPort(TestCase):

    def test_port(self):
        res = monitoring.check_port('ftp.mozilla.org', 21)
        self.assertTrue(res['valid'])
        self.assertTrue(res['status_ok'])

    def test_port_with_content(self):
        res = monitoring.check_port('ftp.mozilla.org', 21, 'Mozilla')
        self.assertTrue(res['valid'])
        self.assertTrue(res['status_ok'])

    def test_closed_port(self):
        res = monitoring.check_port('ftp.mozilla.org', 125)
        self.assertFalse(res['valid'])
