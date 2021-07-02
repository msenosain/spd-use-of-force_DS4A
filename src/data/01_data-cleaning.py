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
    df['GO Num'] = df['GO Num'].fillna(0).astype(np.int64)
    ## Converted to datetime
    df['First Dispatch Time'] = pd.to_datetime(df['First Dispatch Time'], errors='coerce')
    df['Clear Time'] = pd.to_datetime(df['Clear Time'], errors='coerce')
    ## Drop NaN values
    df.dropna(subset=['First Dispatch Time', 'Clear Time', 'Total Service Time'], inplace=True)
    ## Create new cols from datetime data
    df['Total Service Time'] = pd.to_datetime(df['Total Service Time'], unit = 's').dt.minute.astype(int) #Convert to minute
    df['First Dispatch Year'] = df['First Dispatch Time'].dt.year.astype(int)
    df['First Dispatch Month'] = df['First Dispatch Time'].dt.month.astype(int)
    df['First Dispatch Weekday'] = df['First Dispatch Time'].dt.weekday.astype(int)
    df['First Dispatch Hour'] = df['First Dispatch Time'].dt.hour.astype(int)
    df['Clear Year'] = df['Clear Time'].dt.year.astype(int)
    df['Clear Month'] = df['Clear Time'].dt.month.astype(int)
    df['Clear Weekday'] = df['Clear Time'].dt.weekday.astype(int)
    df['Clear Hour'] = df['Clear Time'].dt.hour.astype(int)
    ## Edit some datetime errors
    df['Clear Year'] = df['Clear Year'].replace(1900, 2019)
    df.loc[df['Year']==2020,'First Dispatch Year'] = 2020
    df.loc[df['Year']==2020,'Clear Year'] = 2020
    df = df[df['First Dispatch Year']==df['Year']] #First dispatch year == Year
    df = df[df['Clear Year']>=df['Year']] #Clear Year >= Year
    ## Fix CAD Event ID to match with other datasets
    df["CAD Event ID"].astype(str).apply(lambda x: x[:4] + "0" + x[4:] if len(x) == 13 else x)

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
    ## Change GO column titles to be consistent with one another
    df=df.rename(columns={"GO": "GO Num"})
    #drop GO Num entries with typos
    typo_list = ['2020=197851', '20210000O27515', '2021=056435', '20 21000069987']
    df.drop(df.loc[df["GO Num"].isin(typo_list)].index, inplace=True)

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
    df['Exhibiting Behavior (group)'] = df['Exhibiting Behavior (group)'].str.replace ("BEHAVIOR - ", "", regex = True)
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
    df['Subject Gender'] = df['Subject Gender'].str.upper()
    df['Subject Race'] = df['Subject Race'].str.upper()

    ## Modifying column names
    df = df.rename(columns = {#'Exhibiting Behavior (group)': 'Behavior',
        'Reported Date (Date)': 'Reported Date',
        'Offense/Incident Ind': 'OffenseIncident'
        #'Subject Age': 'Age',
        #'Subject Gender': 'Gender',
        #'Subject Race': 'Race',
        #'Techniques Used': 'Techniques',
        #'UoF Indicator': 'UoF',
        #'Weapons Involved': 'Weapons'
        })

    ## Specific column edits
    df['Reported Date'] = pd.to_datetime(df['Reported Date'])
    df['Exhibiting Behavior (group)'] = df['Exhibiting Behavior (group)'].str.replace ("BELLIGERENT/UNCOOPERATIVE", 'BELLIGERENT', regex = True)
    df['Exhibiting Behavior (group)'] = df['Exhibiting Behavior (group)'].str.replace ('BELLIGERENT',"BELLIGERENT/UNCOOPERATIVE", regex = True)
    df['Disposition'] = df['Disposition'].replace ("MCT (MOBILE CRISIS TEAM)", "MOBILE CRISIS TEAM" )
    df['Disposition'] = df['Disposition'].replace ("RESOURCES DECLINED", "RESOURCES OFFERED/DECLINED" )
    df['Disposition'] = df['Disposition'].replace ("DMHP REFERRAL", "DMHP/REFERRAL (DCR)" )
    df['Disposition'] = df['Disposition'].replace ("CRISIS CLINIC (CRISIS CONNECTIONS)", "CRISIS CLINIC" )
    df['Disposition'] = df['Disposition'].replace ("SHELTER", "SHELTER / SHELTER TRANSPORT" )
    df['Disposition'] = df['Disposition'].replace ("SHELTER TRANSPORT", "SHELTER / SHELTER TRANSPORT" )
    df['Disposition'] = df['Disposition'].replace ("CASE MANAGER/MH AGENCY NOTIFIED", "MENTAL HEALTH AGENCY OR CASE MANAGER NOTIFIED" )
    df['Disposition'] = df['Disposition'].replace ("DRUG/ALCOHOL TREATMENT REFERRAL", "SOCIAL SERVICE/ALCOHOL AND DRUG/TREATMENT REFERRAL" )
    df['Disposition'] = df['Disposition'].replace ("ARRESTED (REQUIRES ARREST REPORT)", "ARRESTED" )
    df['Disposition'] = df['Disposition'].replace ("SUBJECT ARRESTED", "ARRESTED" )
    df['Disposition'] = df['Disposition'].replace ("NO ACTION POSSIBLE/NECESSARY", "NO ACTION POSSIBLE/NECESSARY/UNABLE TO CONTACT" )
    df['Disposition'] = df['Disposition'].replace ("UNABLE TO CONTACT", "NO ACTION POSSIBLE/NECESSARY/UNABLE TO CONTACT" )
    df['Exhibiting Behavior (group)'] = df['Exhibiting Behavior (group)'].replace ("DISORDERLY", "DISORDERLY/DISRUPTIVE" )
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
