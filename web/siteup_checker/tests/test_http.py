import logging
logger = logging.getLogger(__name__)

from django.test import TestCase

from siteup_checker import monitoring

class TestHttpHeader(TestCase):

    def test_bad_host(self):
        res = monitoring.check_http_header('http://josetomasitotocinito.com')
        self.assertFalse(res['valid'])

    def test_code_mismatch(self):
        res = monitoring.check_http_header('http://httpbin.org/status/200', 404)
        self.assertTrue(res['valid'])
        self.assertFalse(res['status_ok'])
        self.assertEqual(res['status_code'], 200)

    def test_code_match(self):
        res = monitoring.check_http_header('http://httpbin.org/status/404', 404)
        self.assertTrue(res['valid'])
        self.assertTrue(res['status_ok'])
        self.assertEqual(res['status_code'], 404)


class TestHttpContent(TestCase):

    def test_bad_host(self):
        res = monitoring.check_http_content('http://josetomasitotocinito.com')
        self.assertFalse(res['valid'])

    def test_empty_content(self):
        res = monitoring.check_http_content('http://httpbin.org/status/404')
        self.assertTrue(res['valid'])
        self.assertTrue(res['status_ok'])

    def test_found_content(self):
        res = monitoring.check_http_content('http://josetomastocino.com', 'Ingeniero')
        self.assertTrue(res['valid'])
        self.assertTrue(res['status_ok'])

    def test_not_found_content(self):
        res = monitoring.check_http_content('http://josetomastocino.com', 'gay')
        self.assertTrue(res['valid'])
        self.assertFalse(res['status_ok'])
