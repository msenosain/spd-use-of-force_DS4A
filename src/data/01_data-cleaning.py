# Import libraries
import pandas as pd
import numpy as np
import os

# data directories
raw = 'raw'
processed = 'processed'

# datasets filenames
train_uof = 'Miriam VonAschen-Cook - UseOfForceProject-UoF Data w requested fields.xlsx'
cases_pattern = 'Miriam VonAschen-Cook - CAD20'
crisis = 'Miriam VonAschen-Cook - Crisis Report Preliminary Data.xlsx'
crime = 'Miriam VonAschen-Cook - Crime_Data.csv'

##############################################################################
# Training/Use of Force data
##############################################################################
#---------------- Read ----------------#
df = pd.DataFrame(pd.read_excel(os.path.join(raw, train_uof))

#---------------- Clean ----------------#
df.loc[(df['Subject Gender'] == "Male"), "Subject Gender"] = "M"
df.loc[(df['Subject Gender'] == "Female"), "Subject Gender"] = "F"
df.loc[(df['Subject Gender'] == "Not Specified"), "Subject Gender"] = "N"
## Removing leading/trailling spaces from strings
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))

#---------------- Write ----------------#
df.to_csv(os.path.join(processed, 'MVAtrain_cleaned.csv'), index = False)


##############################################################################
# Cases data
##############################################################################
#---------------- Read ----------------#
df = pd.DataFrame()

cases_fn = os.listdir(raw)

for file in cases_fn:
    if file.startswith(cases_pattern):
        f = pd.read_csv(os.path.join(raw,file))
        f['Year'] = int(re.findall("\d+", file)[0])
        df = df.append(f, ignor_index = True)

#---------------- Clean ----------------#
## Removing leading/trailling spaces from strings
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))
## Clean “CAD Event ID” by converting it to integer
df['CAD Event ID'] = df['CAD Event ID'].astype(int)
## Clean “Officer Serial Num” by converting it to integer
df['Officer Serial Num'] = df['Officer Serial Num'].astype(int)
## GO num to integer
df['GO Num'] = df['GO Num'].astype('int64')
## Converted to datetime
df['First Dispatch Time'] = pd.to_datetime(df['First Dispatch Time'])
df['Clear Time'] = pd.to_datetime(df['Clear Time'])
df['Total Service Time'] = pd.to_datetime(df['Total Service Time'], unit = 's').dt.minute #Convert to minute

#---------------- Write ----------------#
df.to_csv(os.path.join(processed, 'MVAallcases_cleaned.csv'), index = False)


##############################################################################
# Crime data
##############################################################################
#---------------- Read ----------------#
df = pd.read_csv(os.path.join(raw, crime))

#---------------- Clean ----------------#
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))
## Change to datetime
df['Offense Start DateTime'] = pd.to_datetime(df['Offense Start DateTime'])
## Make the year column
df['Year'] = df['Offense Start DateTime'].dt.year 
## Drop years before 2015
df.drop(df[df['Year'] < 2015.0].index, inplace = True)
## Year to integer
df['Year'] = df['Year'].astype('int64') #pd.to_numeric(df['Year'], downcast='integer')

#---------------- Write ----------------#
df.to_csv(os.path.join(processed, 'MVAcrime_cleaned.csv'), index = False)


##############################################################################
# Crisis data (preliminary)
##############################################################################
#---------------- Read ----------------#
df = pd.DataFrame(pd.read_excel(crisis))

#---------------- Clean ----------------#
## Removing leading/trailling spaces from strings
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))
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
df.to_csv(os.path.join(processed, 'MVAcrisis_cleaned.csv'), index = False)


