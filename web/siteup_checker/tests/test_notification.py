from datetime import datetime

from django.core import mail
from django.test import TestCase

from siteup_api.models import *
from siteup_checker.tasks_notification import send_notification_email

class TestEmailNotification(TestCase):
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

        self.h1 = PingCheck.objects.create(
            title='Ping Test 1',
            group=g,
            target='google.com'
        )

        self.ls = CheckStatus.objects.create(
            status = 1,
            date_start=datetime.now(),
            check=self.h1
        )

        self.h1.last_status = self.ls
        self.h1.save()

    def test_email_sent(self):
        self.h1.run_check()
        self.assertNotEqual(PingCheck.objects.get().last_status.pk, self.ls.pk)
        send_notification_email(self.h1, self.h1.last_status)

        self.assertEqual(len(mail.outbox), 1)


