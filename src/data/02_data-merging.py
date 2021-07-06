# Import libraries

import numpy as np
import pandas as pd
import os

# Function to merge datasets

def merge_datasets():
    """
    Reads the cleaned datasets and merged them. Only merging crisis, crime and 
    UoF datasets, cases/calls dataset is too big compared to the others and will
    introduce too many NaNs, therefore it is only used to extract the common id
    columns CAD Event ID and GO Num to merge the other datasets.
    

    """

    # Read datasets
    filepath = os.path.join('data', 'processed')
    df_cases = pd.read_csv(os.path.join(filepath, "MVAallcases_cleaned.csv"))
    df_crisis = pd.read_csv(os.path.join(filepath, "MVAcrisis_cleaned.csv"))
    df_crime = pd.read_csv(os.path.join(filepath, "MVAcrime_cleaned.csv"))
    df_uof = pd.read_csv(os.path.join(filepath, "MVAtrain_cleaned.csv"))

    # Create a df from id columns and drop their duplicates
    common_id = (
        df_cases[["CAD Event ID", "GO Num"]]
        .drop_duplicates()
    )

    # dataframe with columns of interest from cases/calls dataset
    df_cases_j = (
        df_cases[["GO Num", "AS Of Officer Title",
        "Clear By Desc", "Call Type Desc", "Call Priority Code", 
        "Total Service Time", "First Dispatch Time", "Clear Time"]]
        .drop_duplicates()
    )

    # Drop "CAD Event ID" = -1 from crisis dataset
    df_crisis.drop(df_crisis[df_crisis["CAD Event ID"] == -1].index, inplace=True)

    # Crisis dataset only has CAD Event ID (no GO Num), so we do an
    # inner join to keep only the rows that can be joined with the other dfs
    df_crisis_j = pd.merge(df_crisis, common_id, how = "inner", on = ["CAD Event ID"])

    # Left join on the crime and uof datasets to the common_id cols to keep everything in crime and uof
    df_crime_j = pd.merge(df_crime, common_id, how = "left", on = ["GO Num"])
    df_uof_j = pd.merge(df_uof, common_id, how = "left", on = ["GO Num"])


    # Outer join to keep all the rows of the datasets
    df_merged = pd.merge(df_crisis_j, df_crime_j, how = "outer", on = ["GO Num"])
    df_merged = pd.merge(df_merged, df_uof_j, how = "outer", on = ["GO Num"])

    # Left join to keep everything in merged and only the necessary rows from cases/calls
    df_merged = pd.merge(df_merged, df_cases_j, how = "left", on = ["GO Num"])

    # Write csv
    df_merged.to_csv(os.path.join(filepath, 'MVA_cleaned_merged.csv'), index = False)

    #(542128, 43)


merge_datasets()
