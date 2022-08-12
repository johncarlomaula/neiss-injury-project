# Import packages
import pandas as pd

# Import variable mappings
df_fmt = pd.read_csv('data/2021_NEISS_FMT.csv')

# Import datasets
df_2017 = pd.read_csv('data/NEISS_2017.csv')
df_2018 = pd.read_csv('data/NEISS_2018.csv')
df_2019 = pd.read_csv('data/NEISS_2019.csv')
df_2020 = pd.read_csv('data/NEISS_2020.csv')
df_2021 = pd.read_csv('data/NEISS_2021.csv')

# Fix column names
df_2021 = df_2021.rename(columns={'Narrative_1': 'Narrative'})
df_2020 = df_2020.rename(columns={'Narrative_1': 'Narrative'})

# Create a list of dataframes
df_list = [df_2017, df_2018, df_2019, df_2020, df_2021]

# Define function to map variable
def get_mapping(variable):
    df_var = df_fmt[df_fmt['Format name'] == variable]
    var_dict = pd.Series(df_var['Format value label'].values, index = df_var['Starting value for format']).to_dict()
    var_dict = {k.replace(' ', ''): v for k, v in var_dict.items()}
    return var_dict

# Get list of format names
formats = df_fmt['Format name'].unique()

# Initialize empty dictionary to contain mappings
mappings = {}

# Get mappings
for name in formats:
    mappings[name] = get_mapping(name)

# Fix age mapping
mappings['AGELTTWO'] = {int(k):round((int(k) - 200) / 12, 3) for k, v in mappings['AGELTTWO'].items() if int(k) > 200}

# Fix alcohol/drug mapping
mappings['ALC_DRUG'] = {int(k):v for k, v in mappings['ALC_DRUG'].items() if k != '.'}

# Fix body part mapping
mappings['BDYPT'] = {int(k):v.split(' - ')[1] for k, v in mappings['BDYPT'].items()}

# Fix diagnosis mapping
mappings['DIAG'] = {int(k):v.split(' - ')[1] for k, v in mappings['DIAG'].items()}

# Fix disposition mapping
mappings['DISP'] = {int(k):v.split(' - ')[1] for k, v in mappings['DISP'].items()}

# Fix fire mapping
mappings['FIRE'] = {int(k):v for k, v in mappings['FIRE'].items()}

# Fix gender mapping
mappings['GENDER'] = {int(k):v for k, v in mappings['GENDER'].items()}

# Fix hispanic mapping
mappings['HISP'] = {int(k):v for k, v in mappings['HISP'].items() if k != '.'}

# Fix location mapping
mappings['LOC'] = {int(k):v for k, v in mappings['LOC'].items()}

# Fix race mapping
mappings['RACE'] = {int(k):v for k, v in mappings['RACE'].items()}

# Fix products mapping
mappings['PROD'] = {int(k) : v.split(' - ')[1] for k, v in mappings['PROD'].items()}

# Define function to map variables
def map_variables(df):
    df['Age'] = df['Age'].replace(mappings['AGELTTWO'])
    df['Sex'] = df['Sex'].replace(mappings['GENDER'])
    df['Race'] = df['Race'].replace(mappings['RACE'])
    df['Hispanic'] = df['Hispanic'].replace(mappings['HISP'])
    df['Body_Part'] = df['Body_Part'].replace(mappings['BDYPT'])
    df['Diagnosis'] = df['Diagnosis'].replace(mappings['DIAG'])
    df['Body_Part_2'] = df['Body_Part_2'].replace(mappings['BDYPT'])
    df['Diagnosis_2'] = df['Diagnosis_2'].replace(mappings['DIAG'])
    df['Disposition'] = df['Disposition'].replace(mappings['DISP'])
    df['Location'] = df['Location'].replace(mappings['LOC'])
    df['Fire_Involvement'] = df['Fire_Involvement'].replace(mappings['FIRE'])
    df['Product_1'] = df['Product_1'].replace(mappings['PROD'])
    df['Product_2'] = df['Product_2'].replace(mappings['PROD'])
    df['Product_3'] = df['Product_3'].replace(mappings['PROD'])
    df['Alcohol'] = df['Alcohol'].replace(mappings['ALC_DRUG'])
    df['Drug'] = df['Drug'].replace(mappings['ALC_DRUG'])
    return df

# Iterate through each dataset and map variables
for df in df_list:
    df = map_variables(df)

# Concatenate dataframes into 1
data = pd.concat(df_list, axis=0)

# Save finalized data to a csv file
data.to_csv('data/NEISS_17-21.csv', index = False)