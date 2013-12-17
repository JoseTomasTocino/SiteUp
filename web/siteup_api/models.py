import re

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save, post_delete
from django.core import validators
from django.core.exceptions import ValidationError

from siteup_checker import monitoring

# Validator OR combination

class ValidateAnyOf(object):
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

# Base models

class BaseCheck(models.Model):
    owner = models.ForeignKey(User, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    target = models.TextField(blank=False)
    check_interval = models.PositiveSmallIntegerField(default=1)
    notify_email = models.BooleanField(default=True)

    logs = generic.GenericRelation('CheckLog')
    last_log_datetime = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        abstract = True

class CheckInList(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    check = generic.GenericForeignKey()

# Concrete models

class PingCheck(BaseCheck):
    should_check_timeout = models.BooleanField(default=False)
    timeout_value = models.PositiveSmallIntegerField(null=True, blank=True,
        validators=[ValidateAnyOf(validators.MaxValueValidator(10),
                                  validators.MinValueValidator(100))])

    def clean(self):
        target_ok = False

        try:
            # Check if it's an IP
            validators.validate_ipv46_address(self.target)
            target_ok = True
        except:
            # Check if it's a hostname
            hostname_regex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$";
            target_ok = re.match(hostname_regex, self.target)

        if not target_ok:
            raise ValidationError('Target should be an IP or a valid hostname')


    def run_check(self):

        if not self.is_active:
            return

        # Fire the ping
        check_result = monitoring.check_ping(self.target)

        # Initialize the log instance
        log = models.CheckLog()
        log.check = self
        log.is_ok = True

        # Ping properly finished
        if check_result['valid']:

            # Save ping average response time
            log.value = check_result['avg']

            # If most pings were received
            if check_result['received'] / check_result['transmitted'] >= 0.5:

                # Check if response time is within boundaries
                if self.should_check_timeout and int(check_result['avg']) > self.timeout_value:
                    log.is_ok = False
                    log.extra = 'Ping max response time exceeded'

            else:
                log.is_ok = False

        # Ping could not be launched
        else:
            log.is_ok = False
            log.extra = 'Incorrect host'

        log.save()
        print log.id


class PortCheck(BaseCheck):
    target_port = models.PositiveSmallIntegerField()
    should_check_response = models.BooleanField(default=False)
    response_value = models.CharField(max_length=255, blank=True)


    def run_check(self):

        if not self.is_active:
            return


class HttpCheck(BaseCheck):
    should_check_status = models.BooleanField(default=True)
    status_value = models.PositiveSmallIntegerField(null=True,
                                                    blank=True,
                                                    validators=[validators.MinValueValidator(100),
                                                                validators.MaxValueValidator(600)])

    should_check_content = models.BooleanField(default=False)
    content_value = models.CharField(max_length=255, blank=True)


    def run_check(self):

        if not self.is_active:
            return

        # Use 404 by default
        status_code = self.status_value if self.should_check_status else 404

        # Send check
        check_result = monitoring.check_http_header(self.target, status_code)

        # Initialize the log instance
        log = models.CheckLog()
        log.check = self

        if check_result['valid']:
            log.value = check_result['status_code']
            log.is_ok = check_result['status_ok']
        else:
            log.is_ok = False

        log.is_ok = check_result['status_ok'] if check_result['valid'] else False

        log.save()

class DnsCheck(BaseCheck):
    resolved_address = models.CharField(max_length=255)
    register_type = models.CharField(max_length=20)


    def run_check(self):

        if not self.is_active:
            return

        check_result = monitoring.check_dns(self.target, self.resolved_address, self.register_type)

        # Initialize the log instance
        log = models.CheckLog()
        log.check = self
        log.is_ok = check_result
        log.save()

# Logging

class CheckLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    is_ok = models.BooleanField(default=True)
    value = models.CharField(max_length=255, blank=True)
    extra = models.TextField(blank=True)
    is_notified = models.BooleanField(default=False)

    # Generic relation to the logged check
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    check = generic.GenericForeignKey()


# Signal handlers

def add_check(sender, **kwargs):
    if 'created' in kwargs and kwargs['created']:
        instance = kwargs['instance']
        ctype = ContentType.objects.get_for_model(instance)
        CheckInList.objects.get_or_create(content_type=ctype,
                                          object_id=instance.id)

def delete_check(sender, **kwargs):
    instance = kwargs['instance']
    object_id = instance.id
    ctype = ContentType.objects.get_for_model(instance)

    CheckInList.objects.get(object_id=object_id, content_type=ctype).delete()

check_types = [PortCheck, HttpCheck, DnsCheck, PingCheck]
for check_type in check_types:
    post_save.connect(add_check, sender=check_type)
    post_delete.connect(delete_check, sender=check_type)