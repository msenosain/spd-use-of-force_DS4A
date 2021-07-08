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

    # Drop "CAD Event ID" = -1 from crisis dataset
    df_crisis.drop(df_crisis[df_crisis["CAD Event ID"] == -1].index, inplace=True)

    # left merge cases to crime dataset
    df_merged = pd.merge(df_cases, df_crime, how = "left", on = ["GO Num"], 
        suffixes = ('_calls', '_crime'))
    # left merge cases+crime to train/uof dataset
    df_merged = pd.merge(df_merged, df_uof, how = "left", on = ["GO Num"], 
        suffixes = ('_crime', '_train'))
    # left merge crisis to cases+crime+train/uof datasets
    df_merged = pd.merge(df_crisis, df_merged, how = "left", on = ["CAD Event ID"],
        suffixes = ('_crisis', '_train'))

    # Write csv
    df_merged.to_csv(os.path.join(filepath, 'MVA_cleaned_merged.csv'), index = False)


merge_datasets()
