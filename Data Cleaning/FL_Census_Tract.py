
# coding: utf-8

# In[1]:

# Cleaning and creation of census 2010 data for the state of Florida
import pandas as pd


# In[2]:

# Import the basic demographic and housing information from census 
census = pd.read_excel('FloridaCensus2010/FL_Census2010_STCOPLCT_BasicRace.xls', sheetname=1, header=1,
                      converters={'STATE':str,'COUNTY':str,'TRACT':str})


# In[3]:

# Filter by SUMLEV 50 which contains county level demographic information
census = census[census['SUMLEV']==140]


# In[4]:

# Remove columns that are completely blank
census = census.dropna(axis=1, how='all')


# In[5]:

# Reindex the dataframe
census.reset_index(drop=True, inplace=True)


# In[6]:

# Create census tract number
census['Id2'] = census['STATE'] + census['COUNTY'] + census['TRACT']


# In[7]:

# Drop the unnecessary columns
census.drop(census.columns[0:5], axis=1, inplace=True)


# In[8]:

# Rename column headers
map_census = {'Id2':'Id2','P0020001':'TOT_POP','P0020002':'TOT_H','P0020005':'TOT_WA','P0020006':'TOT_BA','P0020007':'TOT_IA',
            'P0020008':'TOT_AA','P0020009':'TOT_NA','P0020010':'TOT_OTHER','P0020011':'TOT_TOM','P0040001':'TOT_18+',
            'P0040002':'TOT_H_18+','P0040005':'TOT_WA_18+','P0040006':'TOT_BA_18+','P0040007':'TOT_IA_18+','P0040008':'TOT_AA_18+',
            'P0040009':'TOT_NA_18+','P0040010':'TOT_OTHER_18+','P0040011':'TOT_TOM_18+','H0010001':'TOT_HOUSE_UNITS',
            'H0010002':'OCC_HOUSE_UNITS','H0010003':'VAC_HOUSE_UNITS'}
census = census.rename(index=str, columns=map_census)


# In[9]:

# Rearrange the columns
cols = census.columns.tolist()
cols = cols[-1:] + cols[:-1]
census = census[cols]


# In[10]:

# Import the demographic and housing information
censusDem = pd.read_csv('FloridaCensus2010/DEC_10_SF1_SF1DP1_with_ann.csv', header=1, low_memory=False, converters={'Id2':str})


# In[11]:

# Select the necessary columns for future analysis
censusDem = censusDem[['Id2','Number; SEX AND AGE - Total population - Median age (years)','Percent; SEX AND AGE - Male population',
          'Number; SEX AND AGE - Male population - Median age (years)','Percent; SEX AND AGE - Female population',
         'Number; SEX AND AGE - Female population - Median age (years)','Number; HOUSEHOLDS BY TYPE - Total households - Average household size',
         'Number; HOUSEHOLDS BY TYPE - Total households - Average family size [7]','Number; HOUSING OCCUPANCY - Total housing units - Homeowner vacancy rate (percent) [8]',
         'Number; HOUSING OCCUPANCY - Total housing units - Rental vacancy rate (percent) [9]','Percent; HOUSING TENURE - Occupied housing units - Owner-occupied housing units',
         'Number; HOUSING TENURE - Occupied housing units - Owner-occupied housing units - Average household size of owner-occupied units',
         'Percent; HOUSING TENURE - Occupied housing units - Renter-occupied housing units','Number; HOUSING TENURE - Occupied housing units - Renter-occupied housing units - Average household size of renter-occupied units']]


# In[12]:

# Import the employment information
censusEmp = pd.read_csv('FloridaCensus2010/ACS_10_5YR_S2301_with_ann.csv', header=1, low_memory=False, converters={'Id2':str})


# In[13]:

# Select the necessary columns for future analysis
censusEmp = censusEmp[['Id2','In labor force; Estimate; Population 16 years and over','Employed; Estimate; Population 16 years and over',
                      'Unemployment rate; Estimate; Population 16 years and over']]


# In[14]:

# Import the median income information
censusMhi = pd.read_csv('FloridaCensus2010/ACS_10_5YR_S1903_with_ann.csv', header=1, low_memory=False, converters={'Id2':str})


# In[15]:

censusMhi = censusMhi[['Id2','Median income (dollars); Estimate; Households',
                       'Median income (dollars); Estimate; One race-- - White',
                       'Median income (dollars); Estimate; One race-- - Black or African American',
                       'Median income (dollars); Estimate; One race-- - American Indian and Alaska Native',
                       'Median income (dollars); Estimate; One race-- - Asian',
                       'Median income (dollars); Estimate; One race-- - Native Hawaiian and Other Pacific Islander',
                       'Median income (dollars); Estimate; One race-- - Some other race',
                       'Median income (dollars); Estimate; Two or more races',
                       'Median income (dollars); Estimate; Hispanic or Latino origin (of any race)']]


# In[16]:

# Import the family status information
censusFam = pd.read_csv('FloridaCensus2010/ACS_10_5YR_S1702_with_ann.csv', header=1, low_memory=False, converters={'Id2':str})


# In[17]:

censusFam = censusFam[['Id2','All families  - Total; Estimate; Families','All families  - Percent below poverty level; Estimate; Families',
                      'Married-couple families  - Total; Estimate; Families','Married-couple families  - Percent below poverty level; Estimate; Families',
                      'Female householder, no husband present  - Total; Estimate; Families','Female householder, no husband present  - Percent below poverty level; Estimate; Families']]


# In[18]:

# Import the education level information
censusEdu = pd.read_csv('FloridaCensus2010/ACS_10_5YR_S1501_with_ann.csv', header=1, low_memory=False, converters={'Id2':str})


# In[19]:

censusEdu = censusEdu[["Id2","Total; Estimate; POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL - Less than high school graduate",
                       "Total; Estimate; POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL - High school graduate (includes equivalency)",
                       "Total; Estimate; POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL - Some college or associate's degree",
                       "Total; Estimate; POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL - Bachelor's degree or higher"]]


# In[20]:

# Merge census datasets
census = pd.merge(census, censusDem, how='outer', left_on='Id2', right_on='Id2')
census = pd.merge(census, censusEmp, how='outer', left_on='Id2', right_on='Id2')
census = pd.merge(census, censusMhi, how='outer', left_on='Id2', right_on='Id2')
census = pd.merge(census, censusFam, how='outer', left_on='Id2', right_on='Id2')
census = pd.merge(census, censusEdu, how='outer', left_on='Id2', right_on='Id2')


# In[21]:

# Convert all columns to numeric values and any string to NaN
census = census.apply(pd.to_numeric, errors='coerce')


# In[22]:

# Convert all Nan to 0
census = census.fillna(value=0)


# In[23]:

# Weighted median income for races not belonging to one of the major groups
MHI_WGT_DENOM = (census['Median income (dollars); Estimate; One race-- - American Indian and Alaska Native'] + 
                 census['Median income (dollars); Estimate; One race-- - Native Hawaiian and Other Pacific Islander'] + 
                 census['Median income (dollars); Estimate; One race-- - Some other race'] + 
                 census['Median income (dollars); Estimate; Two or more races'])
MHI_WGT_IA = census['Median income (dollars); Estimate; One race-- - American Indian and Alaska Native'] / MHI_WGT_DENOM
MHI_WGT_IA = MHI_WGT_IA.fillna(value=0)
MHI_WGT_NA = census['Median income (dollars); Estimate; One race-- - Native Hawaiian and Other Pacific Islander'] / MHI_WGT_DENOM
MHI_WGT_NA = MHI_WGT_NA.fillna(value=0)
MHI_WGT_OTHER = census['Median income (dollars); Estimate; One race-- - Some other race'] / MHI_WGT_DENOM
MHI_WGT_OTHER = MHI_WGT_OTHER.fillna(value=0)
MHI_WGT_TOM = census['Median income (dollars); Estimate; Two or more races'] / MHI_WGT_DENOM
MHI_WGT_TOM = MHI_WGT_TOM.fillna(value=0)
MHI_OTHER = (census['Median income (dollars); Estimate; One race-- - American Indian and Alaska Native'] * MHI_WGT_IA + 
             census['Median income (dollars); Estimate; One race-- - Native Hawaiian and Other Pacific Islander'] * MHI_WGT_NA + 
             census['Median income (dollars); Estimate; One race-- - Some other race'] * MHI_WGT_OTHER + 
             census['Median income (dollars); Estimate; Two or more races'] * MHI_WGT_TOM)
MHI_OTHER = MHI_OTHER.fillna(value=0)
census['MHI_OTHER'] = pd.Series(MHI_OTHER, index=census.index)


# In[24]:

# Rename columns of use
map_census2 = {'Id2':'CENSUS_TRACT','Number; SEX AND AGE - Total population - Median age (years)':'TOT_MED_AGE',
               'Percent; SEX AND AGE - Male population':'PCT_M','Percent; SEX AND AGE - Female population':'PCT_F',
               'Number; SEX AND AGE - Male population - Median age (years)':'M_MED_AGE',
               'Number; SEX AND AGE - Female population - Median age (years)':'F_MED_AGE',
               'Number; HOUSEHOLDS BY TYPE - Total households - Average household size':'AVG_HOUSE_SIZE',
               'Number; HOUSEHOLDS BY TYPE - Total households - Average family size [7]':'AVG_FAM_SIZE',
               'Number; HOUSING OCCUPANCY - Total housing units - Homeowner vacancy rate (percent) [8]':'HOME_VAC_RATE',
               'Number; HOUSING OCCUPANCY - Total housing units - Rental vacancy rate (percent) [9]':'RENT_VAC_RATE',
               'Percent; HOUSING TENURE - Occupied housing units - Owner-occupied housing units':'PCT_OCC_OWNER',
               'Percent; HOUSING TENURE - Occupied housing units - Renter-occupied housing units':'PCT_OCC_RENTER',
               'Number; HOUSING TENURE - Occupied housing units - Owner-occupied housing units - Average household size of owner-occupied units':'AVG_H_SIZE_OWNER',
               'Number; HOUSING TENURE - Occupied housing units - Renter-occupied housing units - Average household size of renter-occupied units':'AVG_H_SIZE_RENTER',
               'In labor force; Estimate; Population 16 years and over':'PCT_LABOR',
               'Employed; Estimate; Population 16 years and over':'PCT_EMP',
               'Unemployment rate; Estimate; Population 16 years and over':'PCT_UNEMP',
               'Median income (dollars); Estimate; Households':'MHI_TOT',
               'Median income (dollars); Estimate; One race-- - White':'MHI_WA',
               'Median income (dollars); Estimate; One race-- - Black or African American':'MHI_BA',
               'Median income (dollars); Estimate; One race-- - Asian':'MHI_AA',
               'Median income (dollars); Estimate; Hispanic or Latino origin (of any race)':'MHI_H',
               'All families  - Total; Estimate; Families':'TOT_FAM',
               'All families  - Percent below poverty level; Estimate; Families':'PCT_FAM_POV',
               'Married-couple families  - Total; Estimate; Families':'TOT_FAM_MARRIED',
               'Married-couple families  - Percent below poverty level; Estimate; Families':'PCT_FAM_MARRIED_POV',
               'Female householder, no husband present  - Total; Estimate; Families':'TOT_FAM_F_ONLY',
               'Female householder, no husband present  - Percent below poverty level; Estimate; Families':'PCT_FAM_F_ONLY_POV',
               'Total; Estimate; POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL - Less than high school graduate':'POV_RATE_NO_GED',
               'Total; Estimate; POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL - High school graduate (includes equivalency)':'POV_RATE_GED',
               "Total; Estimate; POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL - Some college or associate's degree":'POV_RATE_SOME_COL',
               "Total; Estimate; POVERTY RATE FOR THE POPULATION 25 YEARS AND OVER FOR WHOM POVERTY STATUS IS DETERMINED BY EDUCATIONAL ATTAINMENT LEVEL - Bachelor's degree or higher":'POV_RATE_BACH_PLUS'
               }
census = census.rename(index=str, columns=map_census2)


# In[25]:

# Create variables to ease the feature creation process
totPop = census.TOT_POP.sum()
totPop18 = census['TOT_18+'].sum()
totHous = census.TOT_HOUSE_UNITS.sum()
Other = census['TOT_IA'] + census['TOT_NA'] + census['TOT_OTHER'] + census['TOT_TOM']
Other18 = census['TOT_IA_18+'] + census['TOT_NA_18+'] + census['TOT_OTHER_18+'] + census['TOT_TOM_18+']


# In[26]:

# Create additional features:

# Population of a census tract as percent of total population
census['PCT_TOT_POP'] = census.TOT_POP.apply(lambda row: row/totPop)*100

# Hispanic population as a percentage of total population in a census tract
census['PCT_H'] = census.TOT_H.div(census.TOT_POP, axis='index')*100

# White population as a percentage of total population in a census tract
census['PCT_WA'] = census.TOT_WA.div(census.TOT_POP, axis='index')*100

# Black population as a percentage of total population in a census tract
census['PCT_BA'] = census.TOT_BA.div(census.TOT_POP, axis='index')*100

# Asian population as a percentage of total population in a census tract
census['PCT_AA'] = census.TOT_AA.div(census.TOT_POP, axis='index')*100

# Other demographic as a percentage of total population in a census tract
census['PCT_OTHER'] = Other.div(census.TOT_POP, axis='index')*100

# Population of a census tract as percent of total population 18+
census['PCT_TOT_POP_18'] = census['TOT_18+'].apply(lambda row: row/totPop18)*100

# Hispanic population 18+ as a percentage of total population 18+ in a census tract
census['PCT_H_18'] = census['TOT_H_18+'].div(census['TOT_18+'], axis='index')*100

# White population 18+ as a percentage of total population 18+ in a census tract
census['PCT_WA_18'] = census['TOT_WA_18+'].div(census['TOT_18+'], axis='index')*100

# Black population 18+ as a percentage of total population 18+ in a census tract
census['PCT_BA_18'] = census['TOT_BA_18+'].div(census['TOT_18+'], axis='index')*100

# Asian population 18+ as a percentage of total population 18+ in a census tract
census['PCT_AA_18'] = census['TOT_AA_18+'].div(census['TOT_18+'], axis='index')*100

# Population of other races 18+ as a percentage of total population 18+ in a census tract
census['PCT_OTHER_18'] = Other18.div(census['TOT_18+'], axis='index')*100

# Perncentage of occupied housing units by total housing units in a census tract
census['PCT_OCC_HOUSE'] = census.OCC_HOUSE_UNITS.div(census.TOT_HOUSE_UNITS, axis='index')*100

# Perncentage of vacant housing units by total housing units in a census tract
census['PCT_VAC_HOUSE'] = census.VAC_HOUSE_UNITS.div(census.TOT_HOUSE_UNITS, axis='index')*100

# Families as a percentage of total population in a census tract
census['PCT_FAM'] = census.TOT_FAM.div(census.TOT_POP, axis='index')*100

# Married couples as a percentage of total population in a census tract
census['PCT_FAM_MARRIED'] = census.TOT_FAM_MARRIED.div(census.TOT_POP, axis='index')*100

# Female only households as a percentage of total population in a census tract
census['PCT_FAM_F_ONLY'] = census.TOT_FAM_F_ONLY.div(census.TOT_POP, axis='index')*100


# In[27]:

# Drop the unnecessary column from census dataframe
census.drop(census[['Median income (dollars); Estimate; One race-- - American Indian and Alaska Native',
                   'Median income (dollars); Estimate; One race-- - Native Hawaiian and Other Pacific Islander',
                   'Median income (dollars); Estimate; One race-- - Some other race',
                   'Median income (dollars); Estimate; Two or more races']], axis=1, inplace=True)


# In[28]:

# Write the census dataframe to CSV file
census.to_csv('FL_census.csv')

