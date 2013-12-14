from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import os.path

class Command(BaseCommand):
    help =  'Gets the proper command to add to crontab'
    def handle(self, *args, **options):
        cmd =  ['* * * * * cd']
        cmd.append(settings.BASE_DIR)
        cmd.append('&&')
        cmd.append(sys.executable)
        cmd.append(os.path.join(settings.BASE_DIR, 'manage.py'))
        cmd.append('runchecks')
        cmd.append('> /tmp/cronlog.txt 2>&1')
        cmd.append('\n')

        with open('cron_contents.txt', 'w') as f:
            f.write(' '.join(cmd))

        self.stdout.write("A file called 'cron_contents.txt' has been generated. Use")
        self.stdout.write("    crontab cron_contents.txt")
        self.stdout.write("to add the task to your crontab.")
