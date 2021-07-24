# Import libraries

import numpy as np
import pandas as pd
import os

# Function to merge datasets

def merge_datasets():
    """
    Reads the cleaned datasets and merged them.
    

    """

    # Read datasets
    filepath = os.path.join('data', 'processed')
    df_cases = pd.read_csv(os.path.join(filepath, "MVAallcases_cleaned.csv"))
    df_crisis = pd.read_csv(os.path.join(filepath, "MVAcrisis_cleaned.csv"))
    df_crime = pd.read_csv(os.path.join(filepath, "MVAcrime_cleaned.csv"))
    df_uof = pd.read_csv(os.path.join(filepath, "MVAtrain_cleaned.csv"))

    # Drop "CAD Event ID" = -1 from crisis dataset
    df_crisis.drop(df_crisis[df_crisis["CAD Event ID"] == -1].index, inplace=True)

    # drop columns in crisis
    df_crisis.drop(['OffenseIncident'], axis = 1, inplace=True)
    # drop columns in cases
    df_cases.drop(['Officer Dispatch UID', 'Dispatch ID', 'AS Of Officer Title',
        'As_On_Officer Precinct_ID', 'As_On_Officer Precinct_Desc', 
        'As_On_Officer Squad_Desc', 'Partner Officer Serial Num', 
        'Clear By Desc', 'Call Type Desc','Case Type Initial Desc', 
        'Case Type Final Desc','Clear Time','Dispatch Address'], 
        axis = 1, inplace=True)
    # drop columns in crime
    df_crime.drop(['Offense ID', 'Offense Start DateTime', 'Report DateTime', 
        'NIBRS Offense Code', 'Precinct', 'Sector', 'Beat', 'MCPP', 
        '100 Block Address', 'Longitude', 'Latitude', 'Year'], 
        axis = 1, inplace=True)
    # drop columns in uof
    df_uof.drop(['File Num', 'Longitude', 'Latitude', 
        'Officer Title (as of Incident)','Precinct', 'Sector','Subject Gender', 
        'Subject Race', 'Occurred Date'], axis = 1, inplace=True)

    # left merge cases to crime dataset
    df_merged = pd.merge(df_cases, df_crime, how = "left", on = ["GO Num"])
    # left merge cases+crime to train/uof dataset
    df_merged = pd.merge(df_merged, df_uof, how = "left", on = ["GO Num", "Officer Serial Num"])
    # left merge crisis to cases+crime+train/uof datasets
    df_merged = pd.merge(df_crisis, df_merged, how = "left", on = ["CAD Event ID"])

    # Write csv
    df_merged.to_csv(os.path.join(filepath, 'MVA_cleaned_merged.csv'), index = False)


merge_datasets()
