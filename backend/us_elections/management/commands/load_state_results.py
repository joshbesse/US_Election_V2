from django.core.management.base import BaseCommand
import pandas as pd
from us_elections.utils.state_results import join_dfs
from us_elections.models import State, Party, Candidate, StateResults

class Command(BaseCommand):
    help = "Load state results data into StateResults table."

    def handle(self, *args, **options):
        # load state results data
        df_state = pd.read_csv("us_elections/data/1976-2020-president.csv")
        df_2024 = pd.read_excel("us_elections/data/2024_Election.xlsx")

        # join 2000-2020 and 2024 data
        df = join_dfs(df_state, df_2024)

        # map state code to state objects, party to party objects, and candidate name to candidate objects for foreign key relations
        states = {s.state_code: s for s in State.objects.all()}
        parties = {p.party: p for p in Party.objects.all()}
        candidates = {c.candidate_name: c for c in Candidate.objects.all()}

        # iterate through dataframe rows and create StateResults objects
        results = []
        for row in df.itertuples():
            results.append(StateResults(
                year=row.year,
                state=states[row.state_code],
                party=parties[row.party],
                candidate=candidates[row.candidate],
                candidate_votes=row.candidatevotes,
                total_votes=row.totalvotes
            ))

        # bulk insert StateResults objects
        StateResults.objects.bulk_create(results, ignore_conflicts=True)