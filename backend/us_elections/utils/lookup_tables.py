import pandas as pd
from us_elections.models import State, Candidate, Party, County


def prepare_state_data(state_df):
    # zero padding to ensure 2 digit fips code
    state_df["state_fips"] = state_df["state_fips"].apply(lambda fips: str(fips).zfill(2) if len(str(fips)) == 1 else str(fips))

    # change state name to more appealing formatting
    state_df["state"] = state_df["state"].str.title()

    state_info = state_df[["state_fips", "state_po", "state"]].drop_duplicates()

    # list of State objects for bulk insert into db
    states = [State(state_fips=row.state_fips, state_code=row.state_po, state_name=row.state) for row in state_info.itertuples()]
    return states

def prepare_candidate_data(county_df):        
    # filter for democrat and republican candidates
    county_df = county_df[(county_df["party"] == "DEMOCRAT") | (county_df["party"] == "REPUBLICAN")].copy()

    # change candidate name to more appealing formatting
    county_df["candidate"] = county_df["candidate"].str.title()

    # get unique candidates
    candidates_list = county_df["candidate"].unique().tolist()

    # there are 2 different spellings of Donald Trump: Donald Trump and Donald J Trump -> remove Donald Trump
    candidates_list.remove("Donald Trump")

    # list of Candidate objects for bulk insert into db
    candidates = [Candidate(candidate_name=candidate) for candidate in candidates_list]

    return candidates

def prepare_party_data():
    # set parties
    party = ["Democrat", "Republican"]

    # set party colors
    color_hex = ["#0000FF", "#FF0000"]

    # zip parties and colors to store together
    parties_tuples = list(zip(party, color_hex))

    # list of Party objects for bulk insert into db
    parties = [Party(party=party, color_hex=color) for party, color in parties_tuples]

    return parties

def prepare_county_data(county_df):
    # filter for valid fips code of 5 digits
    county_df = county_df[county_df["county_fips"].str.len() == 5]

    # filter for fips code that contains only numbers
    county_df = county_df[county_df["county_fips"].str.isdigit()]

    # get unique combinations of necessary fields
    county_info = county_df[["state_po", "county_name", "county_fips"]].drop_duplicates()

    # map state code to state objects for foreign key relation
    states = {state.state_code: state for state in State.objects.all()}

    # list of County objects for bulk insert into db
    counties = [County(county_fips=row.county_fips, state=states[row.state_po], county_name=row.county_name) for row in county_info.itertuples()]

    return counties