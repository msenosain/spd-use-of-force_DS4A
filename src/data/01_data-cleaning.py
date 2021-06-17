# Import libraries
import pandas as pd
import numpy as np
import sys
import os
import re
import click
from pathlib import Path
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

##############################################################################
# Create data folders
##############################################################################
def create_folders():
    input_filepath = os.path.join('data', 'raw')
    output_filepath = os.path.join('data', 'processed')
    interim_filepath = os.path.join('data', 'interim')
    external_filepath = os.path.join('data', 'external')

    if os.path.isfile(input_filepath):
        raise('data/raw directory already exists')
    else :
        os.makedirs(input_filepath, exist_ok=True)

    if os.path.isfile(output_filepath):
        raise('data/processed directory already exists')
    else :
        os.makedirs(output_filepath, exist_ok=True)

    if os.path.isfile(interim_filepath):
        raise('data/interim directory already exists')
    else :
        os.makedirs(interim_filepath, exist_ok=True)

    if os.path.isfile(external_filepath):
        raise('data/external directory already exists')
    else :
        os.makedirs(external_filepath, exist_ok=True)


##############################################################################
# All datasets
##############################################################################
def clean_all():
    """
    Reads all datasets, cleans them and writes new data
    
    Arguments: 
        input_filepath : path to raw dataset
        output_filepath : path to output folder
    """ 
    clean_uof()
    clean_cases()
    clean_crime()
    clean_crisis()

##############################################################################
# Training/Use of Force data
##############################################################################

def clean_uof():
    """
    Reads the Training/Use of Force dataset, cleans it and writes new data
    
    Arguments: 
        input_filepath : path to raw dataset
        output_filepath : path to output folder
    """
    input_filepath = os.path.join('data', 'raw')
    output_filepath = os.path.join('data', 'processed')
    train_uof = 'Miriam VonAschen-Cook - UseOfForceProject-UoF Data w requested fields.xlsx'

    #---------------- Read ----------------#
    df = pd.DataFrame(pd.read_excel(os.path.join(input_filepath, train_uof)))

    #---------------- Clean ----------------#
    df.loc[(df['Subject Gender'] == "Male"), "Subject Gender"] = "M"
    df.loc[(df['Subject Gender'] == "Female"), "Subject Gender"] = "F"
    df.loc[(df['Subject Gender'] == "Not Specified"), "Subject Gender"] = "N"
    ## Removing leading/trailling spaces from strings
    df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME\\?', '-'))

    #---------------- Write ----------------#
    df.to_csv(os.path.join(output_filepath, 'MVAtrain_cleaned.csv'), index = False)


##############################################################################
# Cases data
##############################################################################

def clean_cases():
    """
    Reads the cases datasets, cleans it and writes new data
    
    Arguments: 
        input_filepath : path to raw dataset
        output_filepath : path to output folder
    """    
    input_filepath = os.path.join('data', 'raw')
    output_filepath = os.path.join('data', 'processed')
    cases_pattern = 'Miriam VonAschen-Cook - CAD20'

    #---------------- Read ----------------#
    df = pd.DataFrame()

    cases_fn = os.listdir(input_filepath)

    for file in cases_fn:
        if file.startswith(cases_pattern):
            f = pd.read_csv(os.path.join(input_filepath,file))
            f['Year'] = int(re.findall("\d+", file)[0])
            df = df.append(f, ignore_index = True)

    #---------------- Clean ----------------#
    ## Removing leading/trailling spaces from strings
    df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME\\?', '-'))
    ## Clean “CAD Event ID” by converting it to integer
    df['CAD Event ID'] = df['CAD Event ID'].astype(int)
    ## Clean “Officer Serial Num” by converting it to integer
    df['Officer Serial Num'] = df['Officer Serial Num'].astype(int)
    ## GO num to integer
    df['GO Num'] = df['GO Num'].astype(int)
    ## Converted to datetime
    # df['First Dispatch Time'] = pd.to_datetime(df['First Dispatch Time'])
    # df['Clear Time'] = pd.to_datetime(df['Clear Time'])
    df['Total Service Time'] = pd.to_datetime(df['Total Service Time'], unit = 's').dt.minute #Convert to minute

    #---------------- Write ----------------#
    df.to_csv(os.path.join(output_filepath, 'MVAallcases_cleaned.csv'), index = False)


##############################################################################
# Crime data
##############################################################################

def clean_crime():
    """
    Reads the crime dataset, cleans it and writes new data
    
    Arguments: 
        input_filepath : path to raw dataset
        output_filepath : path to output folder
    """
    input_filepath = os.path.join('data', 'raw')
    output_filepath = os.path.join('data', 'processed')
    crime = 'Miriam VonAschen-Cook - Crime_Data.csv'

    #---------------- Read ----------------#
    df = pd.read_csv(os.path.join(input_filepath, crime))

    #---------------- Clean ----------------#
    df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME\\?', '-'))
    ## Change to datetime
    df['Offense Start DateTime'] = pd.to_datetime(df['Offense Start DateTime'])
    ## Make the year column
    df['Year'] = df['Offense Start DateTime'].dt.year 
    ## Drop years before 2015 and nan
    df.drop(df[df['Year'] < 2015.0].index, inplace = True)
    df.dropna(subset=['Year'], inplace = True)
    ## Year to integer
    df['Year'] = df['Year'].astype(int) #pd.to_numeric(df['Year'], downcast='integer')

    #---------------- Write ----------------#
    df.to_csv(os.path.join(output_filepath, 'MVAcrime_cleaned.csv'), index = False)


##############################################################################
# Crisis data (preliminary)
##############################################################################

def clean_crisis():
    """
    Reads the crisis dataset, cleans it and writes new data
    
    Arguments: 
        input_filepath : path to raw dataset
        output_filepath : path to output folder
    """ 
    input_filepath = os.path.join('data', 'raw')
    output_filepath = os.path.join('data', 'processed')
    crisis = 'Miriam VonAschen-Cook - Crisis Report Preliminary Data.xlsx'

    #---------------- Read ----------------#
    df = pd.DataFrame(pd.read_excel(os.path.join(input_filepath, crisis)))

    #---------------- Clean ----------------#
    ## Removing leading/trailling spaces from strings
    df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME\\?', '-'))
    ## Specific column edits
    df['Disposition'] = df['Disposition'].str.upper().str.replace (" / ", "/", regex = True)
    df['Exhibiting Behavior (group)'] = df['Exhibiting Behavior (group)'].str.upper().str.replace ("BEHAVIOR – ", "", regex = True)
    df['Exhibiting Behavior (group)'] = df['Exhibiting Behavior (group)'].str.replace (" / ", "/", regex = True)
    df['Exhibiting Behavior (group)'] = df['Exhibiting Behavior (group)'].str.replace ("\xa0", "", regex = True)
    df['Offense/Incident Ind'] = df['Offense/Incident Ind'].str.upper()
    df['Techniques Used'] = df['Techniques Used'].str.upper()
    df['UoF Indicator'] = df['UoF Indicator'].str.replace ("N", "NO", regex = True)
    df['UoF Indicator'] = df['UoF Indicator'].str.replace ("Y", "YES", regex = True)
    df["Weapons Involved"] = df["Weapons Involved"].str.upper()
    df['Weapons Involved'] = df['Weapons Involved'].str.replace("HANDGUN", "FIREARM", regex = True)
    df['Weapons Involved'] = df['Weapons Involved'].str.replace ("RIFLE", "FIREARM", regex = True)
    df['Weapons Involved'] = df['Weapons Involved'].str.replace ("SHOTGUN", "FIREARM", regex = True)
    df['Weapons Involved'] = df['Weapons Involved'].str.replace ("OTHER FIREARM", "FIREARM", regex = True)

    #---------------- Write ----------------#
    df.to_csv(os.path.join(output_filepath, 'MVAcrisis_cleaned.csv'), index = False)


functions = {
    'create_folders': create_folders,
    'clean_all': clean_all,
    'clean_uof': clean_uof,
    'clean_cases': clean_cases,
    'clean_crime': clean_crime,
    'clean_crisis': clean_crisis,
}

if __name__ == '__main__':
    func = functions[sys.argv[1]]
    args = sys.argv[2:]

    sys.exit(func(*args))
