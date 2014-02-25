from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import os.path

class Command(BaseCommand):
    help = 'Outputs the contents for the supervisord gunicorn task'

    def handle(self, *args, **options):
        s = []
        s.append("[program:siteup_gunicorn]")
        s.append("command=" + sys.executable + " " + os.path.join(settings.BASE_DIR, 'manage.py') + " run_gunicorn")
        s.append("directory=" + settings.BASE_DIR)
        s.append("autostart=True")
        s.append("autorestart=True")
        s.append("redirect_stderr=True")
        s.append("stdout_logfile=" + os.path.join(settings.BASE_DIR, 'logs', 'gunicorn.log'))

        self.stdout.write("\n".join(s))
