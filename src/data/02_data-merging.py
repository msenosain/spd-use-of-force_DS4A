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

    # Drop "CAD Event ID" = -1 from crisis dataset
    df_crisis.drop(df_crisis[df_crisis["CAD Event ID"] == -1].index, inplace=True)

    # Crisis dataset only has CAD Event ID (no GO Num), so we do an
    # inner join to keep only the rows that can be joined with the other dfs
    df_crisis_j = pd.merge(df_crisis, common_id, how = "inner", on = ["CAD Event ID"])

    # For the rest of datasets we do an outer join to keep all the rows
    df_merged = pd.merge(df_crisis_j, df_crime, how = "outer", on = ["GO Num"])
    df_merged = pd.merge(df_merged, df_uof, how = "outer", on = ["GO Num"])

    # Write csv
    df_merged.to_csv(os.path.join(filepath, 'MVA_cleaned_merged.csv'), index = False)


merge_datasets()