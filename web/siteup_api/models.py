import logging
logger = logging.getLogger("debugging")
oplogger = logging.getLogger("operations")

from itertools import chain
import re
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from django.core import validators

from siteup_checker import monitoring
from siteup_checker.tasks_notification import enqueue_notification

from .validators import ValidateAnyOf, validate_ip_or_hostname, validate_hostname

from .utils import timedelta_to_string
import managers


####################################################################################
# User related models

class UserExtra(models.Model):
    """
    Extension model to add extra information to the User model.
    """

    user = models.OneToOneField(User)

    send_report = models.BooleanField(
        help_text=_("Receive daily report about all your checks")
    )

    # Device's GCM registration ID
    regid = models.TextField(
        blank=True,
        null=True
    )


####################################################################################
# Log related models

class CheckLog(models.Model):
    """
    Stores the result of the check.
    """

    date = models.DateTimeField(
        auto_now_add=True
    )

    STATUSES = (
        (0, 'Up'),
        (1, 'Down'),
        (2, 'Error'),
    )

    status = models.IntegerField(
        default=0,
        choices=STATUSES
    )

    status_extra = models.CharField(
        max_length=255
    )

    response_time = models.FloatField(
        default=0
    )

    collapse_level = models.IntegerField(
        default=0
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    check = generic.GenericForeignKey('content_type', 'object_id')

    # This is using a custom Model Manager
    objects = managers.CheckLogManager()

    def save(self, update_check=True):
        """Saves itself, then informs the parent Check to see if it needs to create a CheckStatus."""

        super(CheckLog, self).save()

        if update_check:
            self.check.update_status(self)

    def get_status(self):
        return 1 if self.status == 0 else 0


class CheckStatus(models.Model):
    status = models.IntegerField(
        default=0
    )

    status_extra = models.CharField(
        blank=True,
        max_length=255
    )

    date_start = models.DateTimeField()

    date_end = models.DateTimeField(
        null=True
    )

    notified = models.BooleanField(
        default=False
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    check = generic.GenericForeignKey('content_type', 'object_id')

    # This is using a custom Model Manager
    objects = managers.CheckStatusManager()

    def get_date_start(self):
        return self.date_start.isoformat()

    def get_date_end(self):
        if self.date_end:
            return self.date_end.isoformat()
        else:
            return datetime.now().isoformat()

    def get_duration(self):
        return timedelta_to_string(self.date_end - self.date_start + timedelta(seconds=1))


####################################################################################


class BaseCheck(models.Model):
    """
    Base model for the checks. It groups the common fields and relations.
    It's an abstract base class, so no actual table is created for this model.
    """

    title = models.CharField(
        max_length=70,
        help_text=_("Short title for the check")
    )

    description = models.TextField(
        blank=True,
        help_text=_("Larger description, you can include notes.")
    )

    is_active = models.BooleanField(
        default=True,
        help_text=_("Enables or disables the check")
    )

    check_interval = models.PositiveSmallIntegerField(
        default=1,
        help_text=_("In minutes. How often the check should be triggered.")
    )

    notify_email = models.BooleanField(
        default=True,
        help_text=_("Notify changes of the status of this check via email.")
    )

    notify_android = models.BooleanField(
        default=True,
        help_text=_("Notify changes of the status of this check through the Android app (if available).")
    )

    last_log_datetime = models.DateTimeField(
        blank=True,
        null=True
    )

    group = models.ForeignKey('CheckGroup')

    logs = generic.GenericRelation('CheckLog')

    statuses = generic.GenericRelation('CheckStatus')

    last_status = models.ForeignKey('CheckStatus', blank=True, null=True, on_delete=models.SET_NULL)

    def update_status(self, check_log):
        """
        After a check log, this updates the CheckStatus accordingly.
        """

        self.last_log_datetime = check_log.date

        # If status has changed since last time (or there's no previous status)
        if not self.last_status or self.last_status.status != check_log.status:


            # We'll only trigger the new status if there have been some consecutive logs with the same status
            last_n_logs = self.logs.all().order_by('-date')[:settings.CONSECUTIVE_LOGS_FOR_FAILURE]
            last_n_logs_statuses = (x.status for x in last_n_logs)

            # If the N last logs share the same status OR there was no previous status
            if not self.last_status or (len(last_n_logs) == settings.CONSECUTIVE_LOGS_FOR_FAILURE and len(set(last_n_logs_statuses)) == 1):

                oplogger.info(u"STATUS_CHANGE: {} ({}), new status is {}, last status was {}".format(self.title, self.pk, check_log.status, self.last_status.status if self.last_status else "unknown"))

                # Save the new CheckStatus
                s = CheckStatus()
                s.status = check_log.status
                s.status_extra = check_log.status_extra
                s.date_start = check_log.date
                s.check = self
                s.save()

                # If there was a previous status, update its date_end and close it
                if self.last_status and self.last_status.status != check_log.status:
                    self.last_status.date_end = check_log.date
                    self.last_status.save()

                    oplogger.info(u"ENQUEUED_NOTIFICATION: {} ({}), new status is {}, last status was {}".format(self.title, self.pk, check_log.status, self.last_status.status if self.last_status else "unknown"))

                    # Also send notification
                    enqueue_notification(self, s)

                self.last_status = s

        self.save()

    def get_statuses(self):
        return self.statuses.order_by('-date_start')

    def should_run_check(self):
        """Confirms that the check can be run, because it's both active and enough time has passed since the last
        time it ran. """

        if not self.is_active:
            return False

        # If check's just been created, force check
        if self.last_log_datetime is None:
            return True

        # Subtract some seconds from the difference to handle timing deviations
        elapsed_seconds = (datetime.now() - self.last_log_datetime).seconds
        if elapsed_seconds < self.check_interval * 60 - 6:
            logger.info(u"Check %s should not run (elapsed time: %i seconds)" % (self.title, elapsed_seconds))
            return False

        logger.info(u"Check %s will run (elapsed time: %i seconds)" % (self.title, elapsed_seconds))
        return True

    def generic_url(self, action):
        kwargs = { 'pk': self.id, 'type': self.type_name() }
        return reverse(action, kwargs=kwargs)

    def detail_url(self):
        return self.generic_url('view_check')

    def edit_url(self):
        return self.generic_url('edit_check')

    def delete_url(self):
        return self.generic_url('delete_check')

    def enable_url(self):
        return self.generic_url('enablecheck')

    def disable_url(self):
        return self.generic_url('disable_check')

    def unique_name(self):
        return self.__class__.__name__.lower() + str(self.pk)

    def type_name(self):
        return self.__class__.__name__.lower()

    class Meta:
        abstract = True


#######################################################################################################################
# Concrete Check Models

class PingCheck(BaseCheck):

    target = models.CharField(
        max_length=255, blank=False,
        help_text=_("Should be a hostname or an IP"),
        validators=[validate_ip_or_hostname])

    should_check_timeout = models.BooleanField(
        default=False,
        help_text=_("If active, triggers an alarm if the ping is larger than a certain value."))

    timeout_value = models.PositiveSmallIntegerField(
        null=True, blank=True,
        default=200,
        validators=[ValidateAnyOf([validators.MaxValueValidator(1000), validators.MinValueValidator(50)])],
        help_text=_("Maximum timeout for the ping. Only works if previous option is active."))

    def run_check(self, force=False):
        if not self.should_run_check() and not force:
            return

        # Initialize the log instance
        log = CheckLog(check=self)
        log.status = 0

        # Fire the ping
        check_result = monitoring.check_ping(self.target)

        # Ping finished
        if check_result['valid']:

            # Save ping average response time
            log.response_time = check_result['avg']

            # If most pings were received
            if check_result['received'] / check_result['transmitted'] >= 0.5:

                # Check if response time is within boundaries
                if self.should_check_timeout and int(check_result['avg']) > self.timeout_value:
                    log.status = 1
                    log.status_extra = 'Ping max response time exceeded' # TODO: i18n these strings

            # Most pings were lost
            else:
                log.status = 1
                log.status_extra = 'Most packets were lost'

        # Ping could not be launched
        else:
            log.status = 2

            # Check for most common type of error
            if 'error' in check_result and check_result['error'] == 'unknown host':
                log.status_extra = 'Incorrect host'
            else:
                log.status_extra = 'Problem launching Ping'

        logger.info('Save CheckLog, status %i, response_time %i, status_extra "%s"' % (log.status, log.response_time, log.status_extra))
        log.save()

    def __unicode__(self):
        if self.should_check_timeout:
            return _("Ping check to {}, timeout limit {}ms").format(self.target, self.timeout_value)
        else:
            return _("Ping check to {}").format(self.target)

    class Meta:
        verbose_name = _("ping check")
        verbose_name_plural = _("ping checks")


class PortCheck(BaseCheck):

    target = models.CharField(
        max_length=255, blank=False,
        help_text=_("Should be a hostname or an IP"),
        validators=[validate_ip_or_hostname]
    )

    target_port = models.PositiveSmallIntegerField(
        help_text=_("Remote network port to check.<br><div class='more-help'><a href='#'>Click to see common ports</a> <div>21 - FTP<br>22 - SSH<br>25 - SMTP<br>80 - HTTP<br>161 - SNMP<br>443 - HTTPS</div></div>"),
        validators=[validators.MinValueValidator(1),
                    validators.MaxValueValidator(65535)]
    )

    response_check_string = models.CharField(max_length=255, blank=True,
        verbose_name=_("Check for string"),
        help_text=_("Optionally, you can check if the response contains a certain string.")
    )

    def run_check(self, force=False):
        if not self.should_run_check() and not force:
            return

        log = CheckLog(check=self)

        check_result = monitoring.check_port(self.target, self.target_port, self.response_check_string)

        if check_result['valid']:
            if check_result['status_ok']:
                log.status = 0
            else:
                log.status = 1
        else:
            log.status = 2

        log.save()

    def __unicode__(self):
        return _("Port check to port {} of {}").format(self.target_port, self.target)

    class Meta:
        verbose_name = _("port check")
        verbose_name_plural = _("port checks")


class HttpCheck(BaseCheck):

    target = models.CharField(
        max_length=255, blank=False,
        help_text=_("Should be a valid http(s) URL"),
        validators=[validators.URLValidator()])

    status_code = models.PositiveSmallIntegerField(
        default=200,
        help_text=_("HTTP response status code that should be received from the server"),
        validators=[validators.MinValueValidator(100), validators.MaxValueValidator(600)])

    content_check_string = models.CharField(
        max_length=255, blank=True,
        verbose_name=_("Check for string"),
        help_text=_("Optionally, you can check if the response contains a certain string"))


    def run_check(self, force=False):
        if not self.should_run_check() and not force:
            return

        # Initialize the log instance
        log = CheckLog(check=self)

        status_extra = []

        # Send check
        check_result = monitoring.check_http_header(self.target, self.status_code)

        if check_result['valid']:
            status_extra.append("Received status {}.".format(check_result['status_code']))

            if check_result['status_ok']:
                if self.content_check_string.strip():
                    check_result = monitoring.check_http_content(self.target, self.content_check_string.strip())

                    if check_result['status_ok']:
                        status_extra.append("String found.")
                        log.status = 0
                    else:
                        status_extra.append("String not found.")
                        log.status = 1
                else:
                    log.status = 0
            else:
                log.status = 1
        else:
            status_extra.append(check_result['error'])
            log.status = 2

        log.status_extra = ' '.join(status_extra)
        log.save()

    def __unicode__(self):
        return _("Http check to {}, expected status code {}").format(self.target, self.status_code)

    class Meta:
        verbose_name = _("http check")
        verbose_name_plural = _("http checks")


class DnsCheck(BaseCheck):

    target = models.CharField(
        max_length=255, blank=False,
        help_text=_("Should be a hostname"),
        validators=[validate_hostname])

    resolved_address = models.CharField(
        max_length=255, blank=False,
        help_text=_("Should be a valid value for the selected record type"),
    )

    DNS_RECORD_TYPES = (
        ('A', 'A'),
        ('AAAA', 'AAAA'),
        ('CNAME', 'CNAME'),
        ('MX', 'MX'),
        ('TXT', 'TXT')
    )

    record_type = models.CharField(
        max_length=5,
        choices=DNS_RECORD_TYPES,
        default='A',
        help_text=_("Type of dns resource record"))

    def run_check(self, force=False):
        if not self.should_run_check() and not force:
            return

        check_result = monitoring.check_dns(target=self.target,
                                            expected_address=self.resolved_address,
                                            record_type=self.record_type)

        # Initialize the log instance
        log = CheckLog(check=self)

        if check_result['valid']:
            if check_result['status_ok']:
                log.status = 0
            else:
                log.status = 1
        else:
            log.status = 2

        log.save()

    def __unicode__(self):
        return _("DNS check to {}, register type '{}' should resolve to {}").format(self.target, self.record_type, self.resolved_address)

    class Meta:
        verbose_name = _("dns check")
        verbose_name_plural = _("dns checks")


CHECK_TYPES = [DnsCheck, PingCheck, PortCheck, HttpCheck]

###############################################################

class CheckGroup(models.Model):
    """Group of related checks"""
    title = models.CharField(max_length=65,
                             help_text=_("Title for the group of checks"))
    owner = models.ForeignKey(User)

    def __str__(self):
        return _("Check group") + " '" + self.title + "'"

    def checks(self):
        checks = list(chain(self.dnscheck_set.all(), self.pingcheck_set.all(), self.httpcheck_set.all(), self.portcheck_set.all()))

        return checks

    def enable(self):
        for check_type in CHECK_TYPES:
            check_type.objects.filter(group=self).update(is_active=True)

    def disable(self):
        for check_type in CHECK_TYPES:
            check_type.objects.filter(group=self).update(is_active=False)

