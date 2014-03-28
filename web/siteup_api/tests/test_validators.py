import logging
logger = logging.getLogger("debugging")

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from siteup_api.models import *
from siteup_api import validators


class ValidatorsTestCase(TestCase):
    def test_validate_hostname(self):
        try:
            validators.validate_hostname('josetomastocino.com')
        except ValidationError:
            self.fail('validators.validate_hostname failed')

        with self.assertRaises(ValidationError):
            validators.validate_hostname('josetomastocino com')

    def test_validate_ip_or_hostname(self):
        try:
            validators.validate_ip_or_hostname('josetomastocino.com')
            validators.validate_ip_or_hostname('192.168.1.1')
        except ValidationError:
            self.fail('validators.validate_ip_or_hostname failed')

        with self.assertRaises(ValidationError):
            validators.validate_ip_or_hostname('Lorem ipsum dillum sit amet')