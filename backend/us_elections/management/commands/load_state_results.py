from django.core.management.base import BaseCommand
import pandas as pd
from us_elections.utils.state_results import join_dfs

class Command(BaseCommand):
    help = "Load state results data into StateResults table."

    def handle(self, *args, **options):
        # load state results data
        df_state = pd.read_csv("us_elections/data/1976-2020-president.csv")
        df_2024 = pd.read_excel("us_elections/data/2024_Election.xlsx")

        #
        df = join_dfs(df_state, df_2024)
        print(df)

