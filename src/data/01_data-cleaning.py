# Import libraries
import pandas as pd
import numpy as np
import os

# Create a directory for processed data
os.mkdir('cleaned_files')

##############################################################################
# Training/Use of Force data
##############################################################################
# Read
df = pd.DataFrame(pd.read_excel('Miriam VonAschen-Cook - UseOfForceProject-UoF Data w requested fields.xlsx'))

# Clean
df.loc[(df['Subject Gender'] == "Male"), "Subject Gender"] = "M"
df.loc[(df['Subject Gender'] == "Female"), "Subject Gender"] = "F"
df.loc[(df['Subject Gender'] == "Not Specified"), "Subject Gender"] = "N"
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))

# Write
df.to_csv('cleaned_files/MVA-train_cleaned.csv', index = False)

##############################################################################
# Cases data
##############################################################################
# Read

# Concatenate files
df = pd.DataFrame()

cases_fn = os.listdir()

for file in os.listdir():
    if file.startswith("Miriam VonAschen-Cook - CAD20"):
        f = pd.read_csv(file)
        df = df.append(f, ignor_index = True)

# Clean
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))

# Write
df.to_csv('cleaned_files/MVA-allcases_cleaned.csv', index = False)

##############################################################################
# Crime data
##############################################################################
# Read

# Clean
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))

# Write


##############################################################################
# Crisis data
##############################################################################
# Read
df = pd.DataFrame(pd.read_excel('Miriam VonAschen-Cook - Crisis Report Preliminary Data.xlsx'))


# Clean
df.loc[:,df.dtypes == object] = df.loc[:,df.dtypes == object].apply(lambda x: x.str.strip().str.replace('#NAME?', '-'))

# Write
df.to_csv('cleaned_files/MVA-crisis_cleaned.csv', index = False)


