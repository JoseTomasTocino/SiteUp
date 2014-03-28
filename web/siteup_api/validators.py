import re
import logging
logger = logging.getLogger("debugging")

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _


class ValidateAnyOf(object):
    """Receives a list of validators for a model field, and checks
    if ANY of those validators passes. Raises ValidationError otherwise."""

    def __init__(self, validators, message=None):
        self.validators = validators
        self.message = message

    def __call__(self, value):
        messages = []
        params = {}
        errors = []

        for validator in self.validators:
            try:
                validator(value)
                return True
            except ValidationError as e:
                if e.params:
                    errors.append(unicode(e.message) % e.params)
                else:
                    errors.append(unicode(e.message))

        if self.message:
            raise ValidationError(self.message)
        else:
            raise ValidationError('Combined validation failed: ' + ' '.join(errors))


def validate_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)

    if not all(allowed.match(x) for x in hostname.split(".")):
        raise ValidationError(
            _("'%(hostname)s' is not a valid hostname"),
            params={'hostname': hostname}
        )


validate_ip_or_hostname = ValidateAnyOf(validators=[validate_hostname, validators.validate_ipv46_address],
                                        message=_("Target should be a valid IP or hostname"))

    # try:
    #     # Check if it's an IP
    #     validators.validate_ipv46_address(value)
    #     target_ok = True
    # except ValidationError:
    #     # Check if it's a hostname
    #     hostname_regex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    #     target_ok = re.match(hostname_regex, value)

    # if not target_ok:
    #     raise ValidationError('Target should be an IP or a valid hostname')
    # else:
    #     raise ValidationError('lolwut ' + value)
