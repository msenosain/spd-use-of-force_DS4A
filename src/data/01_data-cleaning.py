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
# Read
df = pd.DataFrame(pd.read_excel(os.path.join(raw, train_uof))

# Clean
df.loc[(df['Subject Gender'] == "Male"), "Subject Gender"] = "M"
df.loc[(df['Subject Gender'] == "Female"), "Subject Gender"] = "F"
df.loc[(df['Subject Gender'] == "Not Specified"), "Subject Gender"] = "N"
## Removing leading/trailling spaces from strings
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))

# Write
df.to_csv(os.path.join(processed, 'MVAtrain_cleaned.csv'), index = False)


##############################################################################
# Cases data
##############################################################################
# Read and Concatenate files
df = pd.DataFrame()

cases_fn = os.listdir(raw)

for file in cases_fn:
    if file.startswith(cases_pattern):
        f = pd.read_csv(os.path.join(raw,file))
        f['Year'] = int(re.findall("\d+", file)[0])
        df = df.append(f, ignor_index = True)

# Clean
## Removing leading/trailling spaces from strings
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))
## Clean “CAD Event ID” by converting it to integer
df['CAD Event ID'] = df['CAD Event ID'].astype(int)
## Clean “Officer Serial Num” by converting it to integer
df['Officer Serial Num'] = df['Officer Serial Num'].astype(int)

# Write
df.to_csv(os.path.join(processed, 'MVAallcases_cleaned.csv'), index = False)


##############################################################################
# Crime data
##############################################################################
# Read
df = pd.read_csv()
# Clean
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))

# Write
df.to_csv(os.path.join(processed, 'MVAcrime_cleaned.csv'), index = False)


##############################################################################
# Crisis data
##############################################################################
# Read
df = pd.DataFrame(pd.read_excel(crisis))

# Clean
## Removing leading/trailling spaces from strings
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))

# Write
df.to_csv(os.path.join(processed, 'MVAcrisis_cleaned.csv'), index = False)


