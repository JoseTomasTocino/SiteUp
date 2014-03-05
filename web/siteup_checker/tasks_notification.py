from siteup.celery import app

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _

def enqueue_notification(check, check_status):
    send_notification.delay(check, check_status)

@app.task
def send_notification(check, check_status):
    if check.notify_email:
        send_notification_email(check, check_status)

    # if check.notify_android:
    #     send_notification_android(check, check_status)

def send_notification_email(check, check_status):
    recipient_list = [check.group.owner.email]
    subject = _('[SiteUp] Status report of "{}"').format(check.title[:30] + "...")
    message = """
    Hello.

    This is a status report from SiteUp for your check named "{check_name}".

    The status of the check changed to {new_status} on {status_date}.

    You can check the details at {check_details}.

    Regards.
    The SiteUp team.""".format(
        check_name= check.title,
        new_status= "DOWN"if check_status.status != 0 else "UP",
        status_date= check_status.date_start.isoformat(),
        check_details= ''.join([settings.BASE_URL, reverse("view_check", kwargs={'pk':check.pk, 'type':check.type_name()})]),
    )

    send_mail(
        recipient_list=recipient_list,
        subject=subject,
        message=message,
        from_email="siteup.pfc@gmail.com"
    )






