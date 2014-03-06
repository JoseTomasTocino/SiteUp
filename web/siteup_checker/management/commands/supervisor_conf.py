from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import os, os.path, getpass

class Command(BaseCommand):
    help = 'Outputs the contents for the supervisord configuration file'

    def handle(self, *args, **options):
        base = open(os.path.join(settings.BASE_DIR, 'siteup_checker', 'deployment', 'supervisord_template.conf'), 'r').read()
        template_fields = {
            'VIRTUAL_ENV_DIR': os.environ['VIRTUAL_ENV'],
            'PROJECT_DIR': settings.BASE_DIR,
            'GMAIL_PASS': raw_input('Type the gmail account password: ')
        }

        conf_file_content = base.format(**template_fields)

        self.stdout.write(conf_file_content)
