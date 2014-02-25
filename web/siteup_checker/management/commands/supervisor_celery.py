from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import os, os.path, getpass

class Command(BaseCommand):
    help = 'Outputs the contents for the supervisord celery task'

    def handle(self, *args, **options):
        s = []
        s.append("[program:siteup_gunicorn]")
        binary = os.path.join(os.environ['VIRTUAL_ENV'], 'bin', 'celery') + " worker -B -A siteup -l info -c 16"
        s.append("command=" + binary)
        s.append("directory=" + settings.BASE_DIR)
        s.append("user=" + getpass.getuser())
        s.append("autostart=True")
        s.append("autorestart=True")
        s.append("redirect_stderr=True")
        s.append("stdout_logfile=" + os.path.join(settings.BASE_DIR, 'logs', 'celery.log'))
        self.stdout.write("\n".join(s))
