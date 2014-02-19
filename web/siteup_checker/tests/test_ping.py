import logging
logger = logging.getLogger(__name__)

from django.test import TestCase

from siteup_checker import monitoring

# Create your tests here.

class TestPing(TestCase):

    def test_nonexistent_host(self):
        res = monitoring.check_ping('quwopeiuweropti.es')
        self.assertTrue('valid' in res)
        self.assertFalse(res['valid'])

    def test_existent_host(self):
        res = monitoring.check_ping('josetomastocino.com')
        self.assertTrue('valid' in res)
        self.assertTrue(res['valid'])