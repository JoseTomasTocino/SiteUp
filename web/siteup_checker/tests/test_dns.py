import logging
logger = logging.getLogger(__name__)

from django.test import TestCase

from siteup_checker import monitoring

class TestDns(TestCase):

    def test_wrong_record_type(self):
        # with self.assertRaises(ValueError):
        #     monitoring.check_dns('bad', 'BAD', '1.1.1.1')

        res = monitoring.check_dns('bad', 'BAD', '1.1.1.1')
        self.assertFalse(res['valid'])

    def test_wrong_host(self):
        res = monitoring.check_dns('josetomasitotocinote.com', 'A', '1.1.1.1')
        self.assertFalse(res['valid'])

    def test_wrong_resolved_address(self):
        res = monitoring.check_dns('josetomastocino.com', 'A', '1.1.1.1')
        self.assertTrue(res['valid'])
        self.assertFalse(res['status_ok'])

    def test_valid(self):
        res = monitoring.check_dns('josetomastocino.com', 'A', '78.47.140.228')
        self.assertTrue(res['valid'])
        self.assertTrue(res['status_ok'])