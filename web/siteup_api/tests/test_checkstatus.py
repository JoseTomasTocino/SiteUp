import logging
logger = logging.getLogger(__name__)

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from siteup_api.models import *
from siteup_api import validators

class CheckStatusTestCase(TestCase):
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

    def test_check_status_created(self):
        for i in range(settings.CONSECUTIVE_LOGS_FOR_FAILURE - 1):
            self.h1.run_check(force=True)
            self.assertFalse(CheckStatus.objects.all())
            self.assertEqual(len(self.h1.logs.all()), i + 1)

        self.h1.run_check(force=True)
        self.assertEqual(len(CheckStatus.objects.all()), 1)
