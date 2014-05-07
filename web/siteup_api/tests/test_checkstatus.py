import logging
logger = logging.getLogger("debugging")

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
            consecutive_logs_for_failure=4,
            target='http://josetomastocino.com'
        )

    def test_check_status_created(self):
        # Run check for first time
        self.h1.run_check(force=True)

        # Refresh the pointer
        self.h1 = HttpCheck.objects.get()

        # There should 1 CheckLog and 1 CheckStatus associated to the Check
        self.assertEqual(len(CheckStatus.objects.all()), 1)
        self.assertEqual(len(CheckLog.objects.all()), 1)
        self.assertIsNotNone(self.h1.last_status)
        self.assertEqual(len(self.h1.statuses.all()), 1)
        self.assertEqual(len(self.h1.logs.all()), 1)

        # Change the target so now it fails
        self.h1.target='http://josetomastocinoasd.com'
        self.h1.save()

        # Trigger the check enough times to raise a new CheckStatus
        for i in range(self.h1.consecutive_logs_for_failure):
            self.assertEqual(len(CheckStatus.objects.all()), 1)
            self.h1.run_check(force=True)
            self.assertEqual(len(self.h1.logs.all()), i + 2)

        logger.info(self.h1.consecutive_logs_for_failure)

        # Now there should be TWO CheckStatus objects
        self.h1 = HttpCheck.objects.get()
        self.assertEqual(len(self.h1.statuses.all()), 2)
        self.assertEqual(len(CheckStatus.objects.all()), 2)


