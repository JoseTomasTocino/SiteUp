from multiprocessing import Pool
from datetime import datetime

from django.core.management.base import BaseCommand

from siteup_api import models

class Command(BaseCommand):
    """
    Adds a 'runcheck' Django command to run all the active checks.
    """

    help = 'Runs all the active checks'

    def handle(self, *args, **options):

        print "Runcheck", str(datetime.now())

        # Get all checks
        checks = models.CheckInList.objects.all()

        # Build a process pool to handle checks in parallel
        pool = Pool(processes=30)

        # Run each check
        pool.map_async(run_single_check, checks)

        # Wait for all the checks to finish
        pool.close()
        pool.join()

def run_single_check(check):
    print "Running check:", check.check.title

    return check.check.run_check()