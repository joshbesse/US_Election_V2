from django.core.management.base import BaseCommand
import pandas as pd
from us_elections.models import State, Candidate, Party, County
from us_elections.utils.lookup_tables import prepare_state_data, prepare_candidate_data, prepare_party_data, prepare_county_data

class Command(BaseCommand):
    help = "Load data into look up tables (State, Candidate, Party, County)."

    def handle(self, *args, **options):
        state_df = pd.read_csv("us_elections/data/1976-2020-president.csv")
        county_df = pd.read_csv("us_elections/data/countypres_2000-2024.csv")

        # Insert state data into State table
        states = prepare_state_data(state_df)
        State.objects.bulk_create(states, ignore_conflicts=True)

        # Insert candidate data into Candidate table
        candidates = prepare_candidate_data(county_df)
        Candidate.objects.bulk_create(candidates, ignore_conflicts=True)

        # Insert party data into Party table
        parties = prepare_party_data()
        Party.objects.bulk_create(parties, ignore_conflicts=True)

        # Insert county data into County table
        counties = prepare_county_data(county_df)
        County.objects.bulk_create(counties, ignore_conflicts=True)