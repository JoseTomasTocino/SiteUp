import sys
import os
import os.path
import getpass

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Outputs the contents for the supervisor configuration file'

    def handle(self, *args, **options):
        base = open(os.path.join(settings.BASE_DIR, 'siteup_checker', 'deployment', 'supervisor_template.conf'), 'r').read()
        template_fields = {
            'VIRTUAL_ENV_DIR': os.environ['VIRTUAL_ENV'],
            'PROJECT_DIR': settings.BASE_DIR,
            'PROJECT_LOG_DIR': os.path.abspath(os.path.join(settings.BASE_DIR, '..', 'logs')),
            'GMAIL_PASS': raw_input('Type the gmail account password: '),
            'GCM_API_KEY': raw_input('Type your GCM API key: ')
        }

        conf_file_content = base.format(**template_fields)

        output_file = open(os.path.join(settings.BASE_DIR, 'supervisor-siteup.conf'), 'w')
        output_file.write(conf_file_content)
        output_file.close()

        self.stdout.write("Supervisor configuration written to 'supervisor-siteup.conf'")
