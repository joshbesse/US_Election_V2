import pandas as pd

def format_name(name):
    # split name on comma to get first and last names
    last, first = name.split(",")

    return f"{first} {last}".strip().title()   

def clean_state_df(df_state):
    # drop and rename columns to match other df
    df_state = df_state.drop(["state_fips", "state_cen", "state_ic", "office", "party_detailed", "writein", "version", "notes"], axis=1)
    df_state = df_state.rename(columns={"state_po": "state_code", "party_simplified": "party"})

    # filter for correct timeframe, wanted parties, and valid candidates
    df_state = df_state[df_state["year"] >= 2000]
    df_state = df_state[(df_state["party"] == "DEMOCRAT") | (df_state["party"] == "REPUBLICAN")]
    df_state = df_state[(~df_state["candidate"].isna()) & (df_state["candidate"] != "OTHER")]

    # drop error rows (2016 Maryland had 2 extra rows)
    df_state = df_state.drop([3542, 3543])

    return df_state

def join_dfs(df_state, df_2024):       
    # clean 2000-2020 data
    df_state = clean_state_df(df_state)

    # combine 2000-2020 and 2024 data
    df_combined = pd.concat([df_state, df_2024])

    # ensure candidate format matches Candidate table
    df_combined["candidate"] = df_combined["candidate"].apply(format_name)
    df_combined["candidate"] = df_combined["candidate"].replace({
        "Barack H. Obama": "Barack Obama",
        "John Mccain": "John McCain",
        "Donald J. Trump": "Donald Trump",
        "Joseph R. Jr Biden": "Joe Biden"
    })

    # ensure party format matches Party table
    df_combined["party"] = df_combined["party"].str.title()

    return df_combined