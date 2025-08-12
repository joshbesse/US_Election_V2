from django.core.management.base import BaseCommand
import pandas as pd

class Command(BaseCommand):
    help = "Clean presidential election results by state data"

    def handle(self, *args, **options):
        df = pd.read_csv("us_elections/data/1976-2020-president.csv")
        #df = pd.read_csv("us_elections/data/countypres_2000-2024.csv")
        print(df.head(40))