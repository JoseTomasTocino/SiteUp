import logging
logger = logging.getLogger(__name__)

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from siteup_api.models import *
from siteup_api import validators

class HttpTestCase(TestCase):
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

        self.h1 = HttpCheck.objects.create(
            title='HTTP Test 1',
            group=g,
            target='http://josetomastocino.com'
        )

        self.h2 = HttpCheck.objects.create(
            title='HTTP Test 2',
            group=g,
            target='http://josetomastocino.com',
            content_check_string='Ingeniero'
        )

        self.h3 = HttpCheck.objects.create(
            title='HTTP Test 1',
            group=g,
            target='http://httpbin.org/status/404'
        )

        self.h4 = HttpCheck.objects.create(
            title='HTTP Test 1',
            group=g,
            target='http://josetomastinoticinas.com'
        )

    def test_http_up(self):
        self.h1.run_check()
        check_log = self.h1.logs.get()
        self.assertEqual(check_log.status, 0)

    def test_http_up_with_content(self):
        self.h2.run_check()
        check_log = self.h2.logs.get()
        self.assertEqual(check_log.status, 0)

    def test_http_404(self):
        self.h3.run_check()
        check_log = self.h3.logs.get()
        self.assertEqual(check_log.status, 1)
        self.assertEqual(check_log.status_extra, '404')

    def test_http_bad_host(self):
        self.h4.run_check()
        check_log = self.h4.logs.get()
        self.assertEqual(check_log.status, 2)