import pandas as pd

def clean_county_fips(county_df):
    # filter for valid fips code
    county_df = county_df[county_df["county_fips"].str.len() == 5]
    county_df = county_df[county_df["county_fips"].str.isdigit()]

    # filter for valid parties and ensure correct formatting
    county_df = county_df[(county_df["party"] == "DEMOCRAT") | (county_df["party"] == "REPUBLICAN")]
    county_df["party"] = county_df["party"].str.title()

    # ensure correct candidate formatting
    county_df["candidate"] = county_df["candidate"].str.title()
    county_df["candidate"] = county_df["candidate"].replace({
        "John Mccain": "John McCain",
        "Donald J Trump": "Donald Trump",
        "Joseph R Biden Jr": "Joe Biden",
        "Kamala D Harris": "Kamala Harris"
    })

    return county_df