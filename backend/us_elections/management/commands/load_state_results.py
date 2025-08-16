from django.core.management.base import BaseCommand
import pandas as pd

class Command(BaseCommand):
    help = "Clean presidential election results by state data"

    def handle(self, *args, **options):
        df = pd.read_csv("us_elections/data/1976-2020-president.csv")

        # State
        df["state_fips"] = df["state_fips"].apply(lambda fips: str(fips).zfill(2) if len(str(fips)) == 1 else str(fips))
        state_fips = df["state_fips"].unique()

        state_code = df["state_po"].unique()

        df["state"] = df["state"].str.title()
        state_name = df["state"].unique()

        # Candidate
        df["candidate"] = df["candidate"].str.title()
        candidate_name = df["candidate"].unique()

        # Party
        df["party_simplified"] = df["party_simplified"].str.title()
        party_simplified = df["party_simplified"].unique()

        df["party_detailed"] = df["party_detailed"].str.title()
        party_detailed = df["party_detailed"].unique()

        color_hex = ["#0000FF", "#FF0000", "#9D00FF", "#FFA500"]

        # StateResults