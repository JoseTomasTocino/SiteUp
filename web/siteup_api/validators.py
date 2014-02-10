import re

from django.core import validators
from django.core.exceptions import ValidationError


class ValidateAnyOf(object):
    """Receives a list of validators for a model field, and checks
    if ANY of those validators passes. Raises ValidationError otherwise."""

    def __init__(self, *validators):
        self.validators = validators

    def __call__(self, value):
        errors = []
        for validator in self.validators:
            try:
                validator(value)
                return
            except ValidationError as e:
                errors.append(unicode(e.message) % e.params)

        raise ValidationError('Combined validation failed: ' + ' '.join(errors))


def validate_ip_or_hostname(value):
    try:
        # Check if it's an IP
        validators.validate_ipv46_address(value)
        target_ok = True
    except ValidationError:
        # Check if it's a hostname
        hostname_regex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
        target_ok = re.match(hostname_regex, value)

    if not target_ok:
        raise ValidationError('Target should be an IP or a valid hostname')
