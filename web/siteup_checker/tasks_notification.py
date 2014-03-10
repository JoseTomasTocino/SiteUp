import logging
oplogger = logging.getLogger("operations")

from siteup.celery import app

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def enqueue_notification(check, check_status):
    send_notification.delay(check, check_status)

@app.task
def send_notification(check, check_status):
    if check.notify_email:
        send_notification_email(check, check_status)

    # if check.notify_android:
    #     send_notification_android(check, check_status)

def send_notification_email(check, check_status):
    from_email = "siteup.pfc@gmail.com"
    recipient_list = [check.group.owner.email]
    subject = _('[SiteUp] Status report of "{}"').format(check.title[:30] + "...")
    message_html = render_to_string('email_status_report.html', {
        "check_name": check.title,
        "new_status": "DOWN" if check_status.status != 0 else "UP",
        "status_date": check_status.date_start.isoformat(),
        "check_details": ''.join([settings.BASE_URL, reverse("view_check", kwargs={'pk':check.pk, 'type':check.type_name()})]),
    })

    message_text = strip_tags(message_html)

    mail = EmailMultiAlternatives(subject, message_text, from_email, recipient_list)
    mail.attach_alternative(message_html, "text/html")
    mail.send()







