import logging
logger = logging.getLogger(__name__)
oplogger = logging.getLogger("operations")

from siteup.celery import app

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def enqueue_notification(check, check_status):
    """
    Enqueues a generic notification task
    """

    return send_notification.delay(check, check_status)


@app.task
def send_notification(check, check_status):
    """
    Triggers both email and android notifications
    """

    if check.notify_email:
        send_notification_email(check, check_status)

    if check.notify_android:
        send_notification_android(check, check_status)

def send_notification_email(check, check_status):
    """
    Sends an email notifying of a change in the status of a check.
    """

    logger.info("Sending notification mail...")

    from_email = "siteup.pfc@gmail.com"
    recipient_list = [check.group.owner.email]
    subject = _('[SiteUp] Status report of "{}"').format(check.title[:30] + "...")
    message_html = render_to_string('email_status_report.html', {
        "check_name": check.title,
        "new_status": "DOWN" if check_status.status != 0 else "UP",
        "status_date": check_status.date_start,
        "check_details": ''.join([settings.BASE_URL, reverse("view_check", kwargs={'pk':check.pk, 'type':check.type_name()})]),
    })

    message_text = strip_tags(message_html)

    mail = EmailMultiAlternatives(subject, message_text, from_email, recipient_list)
    mail.attach_alternative(message_html, "text/html")
    mail.send()


def send_notification_android(check, check_status):
    """
    Sends a PUSH notification through GCM to the check owner's Android app.
    """

    pass



@periodic_task(run_every=crontab(hour="0", minute="0", day_of_week="*"))
def send_daily_reports():
    """
    Sends daily reports to those users that activated the option.
    """

    for user in User.objects.all():

        # Some users may not have an associated UserExtra model
        try:
            should_send_report = user.userextra.send_report
        except:
            should_send_report = True

        # Continue with the next user in case the report must not be sent
        if not should_send_report:
            continue

        # Get the checks for the current user
        context = {}
        context['check_groups'] = user.checkgroup_set \
            .prefetch_related('dnscheck_set', 'pingcheck_set', 'httpcheck_set', 'portcheck_set')

        for check_group in context['check_groups']:
            check_group.checks = []
            check_group.checks.extend(check_group.dnscheck_set.all())
            check_group.checks.extend(check_group.pingcheck_set.all())
            check_group.checks.extend(check_group.httpcheck_set.all())
            check_group.checks.extend(check_group.portcheck_set.all())


        from_email = "siteup.pfc@gmail.com"
        recipient_list = [user.email]
        subject = _('[SiteUp] Daily status report')
        message_html = render_to_string('email_daily_report.html', context)
        message_text = strip_tags(message_html)

        mail = EmailMultiAlternatives(subject, message_text, from_email, recipient_list)
        mail.attach_alternative(message_html, "text/html")
        mail.send()












