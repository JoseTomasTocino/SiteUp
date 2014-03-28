import logging
logger = logging.getLogger("debugging")

from django.test import TestCase

from siteup_checker import monitoring

class TestPing(TestCase):

    def test_invalid_host(self):
        res = monitoring.check_ping('josetomasitotocinote.com')
        self.assertTrue('valid' in res)
        self.assertFalse(res['valid'])

    def test_valid_host(self):
        res = monitoring.check_ping('josetomastocino.com')
        self.assertTrue('valid' in res)
        self.assertTrue(res['valid'])