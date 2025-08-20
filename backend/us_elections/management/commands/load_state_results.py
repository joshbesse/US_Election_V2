from django.core.management.base import BaseCommand
import pandas as pd

class Command(BaseCommand):
    help = "Load state results data into StateResults table."

    def handle(self, *args, **options):
        