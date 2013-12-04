from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

# Create your models here.

class Check(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    target = models.TextField()
    check_interval = models.PositiveSmallIntegerField()
    notify_email = models.BooleanField(default=True)

    logs = generic.GenericRelation('CheckLog')

    class Meta:
        abstract = True


class PingCheck(Check):
    should_check_timeout = models.BooleanField(default=False)
    timeout_value = models.PositiveSmallIntegerField(blank=True)


class PortCheck(Check):
    target_port = models.PositiveSmallIntegerField()
    should_check_response = models.BooleanField(default=False)
    response_value = models.CharField(max_length=255, blank=True)


class HttpCheck(Check):
    should_check_status = models.BooleanField(default=True)
    status_value = models.PositiveSmallIntegerField(blank=True)
    should_check_content = models.BooleanField(default=False)
    content_value = models.CharField(max_length=255, blank=True)


class DnsCheck(Check):
    resolved_address = models.CharField(max_length=255)
    register_type = models.CharField(max_length=20)

class CheckLog(models.Model):
    date = models.DateTimeField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    check = generic.GenericForeignKey()



