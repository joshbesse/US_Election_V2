from django.core.management.base import BaseCommand
import pandas as pd
from us_elections.utils.county_results import clean_county_fips
from us_elections.models import County, Party, Candidate, CountyResults

class Command(BaseCommand):
    help = "Load county results data into CountyResults table."

    def handle(self, *args, **options):
        # load county results data
        county_df = pd.read_csv("us_elections/data/countypres_2000-2024.csv")

        # clean data to ensure valid rows and correct formatting
        county_df = clean_county_fips(county_df)

        # map county fips to county objects, party to party objects, and candidate name to candidate objects for foreign key relations
        counties = {c.county_fips: c for c in County.objects.all()}
        parties = {p.party: p for p in Party.objects.all()}
        candidates = {ca.candidate_name: ca for ca in Candidate.objects.all()}

        # iterate through dataframe rows and create CountyResults objects
        results = []
        for row in county_df.itertuples():
            results.append(CountyResults(
                year=row.year,
                county=counties[row.county_fips],
                party=parties[row.party],
                candidate=candidates[row.candidate],
                candidate_votes=row.candidatevotes,
                total_votes = row.totalvotes
            ))
        
        # bulk insert CountyResults objects
        CountyResults.objects.bulk_create(results, batch_size=5000, ignore_conflicts=True)