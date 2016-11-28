
# coding: utf-8

# In[1]:

# Cleaning and creation of census 2010 data for the state of Florida
import pandas as pd


# In[2]:

# Import the population demographic information
censusDemo = pd.read_csv('FloridaCensus2010/CC-EST2015-ALLDATA-12.csv', header=0)


# In[3]:

# Filter by total census population 
censusDemo = censusDemo[(censusDemo.YEAR == 1) & (censusDemo.AGEGRP == 0)]


# In[4]:

# Reindex the censusDemo dataframe
censusDemo.reset_index(drop=True, inplace=True)


# In[5]:

# Drop the unnecessary columns
censusDemo.drop(censusDemo.columns[58:80], axis=1, inplace=True)
censusDemo.drop(censusDemo.columns[34:56], axis=1, inplace=True)
censusDemo.drop(censusDemo.columns[22:32], axis=1, inplace=True)
censusDemo.drop(censusDemo.columns[[0,1,3,5,6]], axis=1, inplace=True)


# In[6]:

# Import another population demographic file
censusDemo2 = pd.read_excel('FloridaCensus2010/FL_Census2010_STCOPLCT_BasicRace.xls', sheetname=1, header=1)


# In[7]:

# Filter by SUMLEV 50 which contains county level demographic information
censusDemo2 = censusDemo2[censusDemo2['SUMLEV']==50]


# In[8]:

# Remove columns that are completely blank
censusDemo2 = censusDemo2.dropna(axis=1, how='all')


# In[9]:

# Reindex the censusDemo2 dataframe
censusDemo2.reset_index(drop=True, inplace=True)


# In[10]:

# Drop the unnecessary columns
censusDemo2.drop(censusDemo2.columns[[0,1,3,4]], axis=1, inplace=True)


# In[11]:

# Rename column headers
map_Demo2 = {'COUNTY':'COUNTY','NAME':'CTYNAME','P0020002':'TOT_H','P0020005':'TOT_WA','P0020006':'TOT_BA','P0020007':'TOT_IA',
            'P0020008':'TOT_AA','P0020009':'TOT_NA','P0020010':'TOT_OTHER','P0020011':'TOT_TOM','P0040001':'TOT_18+',
            'P0040002':'TOT_H_18+','P0040005':'TOT_WA_18+','P0040006':'TOT_BA_18+','P0040007':'TOT_IA_18+','P0040008':'TOT_AA_18+',
            'P0040009':'TOT_NA_18+','P0040010':'TOT_OTHER_18+','P0040011':'TOT_TOM_18+','H0010001':'TOT_HOUS_UNITS',
            'H0010002':'OCC_HOUS_UNITS','H0010003':'VAC_HOUS_UNITS'}
censusDemo2 = censusDemo2.rename(index=str, columns=map_Demo2)


# In[12]:

# Merge demographic dataframes together
census = censusDemo.merge(censusDemo2, left_on='COUNTY', right_on='COUNTY', how='outer')


# In[13]:

# Load in the median household income and other addtional data for 2010 census
censusExtra = pd.read_csv('FloridaCensus2010/FL_census_extra.csv', header=0)


# In[14]:

# Drop the unnecessary column
censusExtra.drop(censusExtra.columns[[1]], axis=1, inplace=True)


# In[15]:

# Merge census dataframe with extra information
census = census.merge(censusExtra, left_on='COUNTY', right_on='County number', how='outer')


# In[16]:

# Drop the unnecessary column from census dataframe
census.drop(census[['County number']], axis=1, inplace=True)


# In[17]:

# Create variables to ease the feature creation process
totPop = census.TOT_POP.sum()
totPop18 = census['TOT_18+'].sum()
totM = census.TOT_MALE.sum()
totF = census.TOT_FEMALE.sum()
totHous = census.TOT_HOUS_UNITS.sum()
Other = census['TOT_IA'] + census['TOT_NA'] + census['TOT_OTHER'] + census['TOT_TOM']
Other18 = census['TOT_IA_18+'] + census['TOT_NA_18+'] + census['TOT_OTHER_18+'] + census['TOT_TOM_18+']


# In[18]:

# Create additional features by total population of a predictor in the state of Florida:

# Population of a county as percent of total population
census['Pop as % of total Pop'] = census.TOT_POP.apply(lambda row: row/totPop*100)

# Male population of a county as a percentage of total population
census['M Pop as % of total Pop'] = census.TOT_MALE.apply(lambda row: row/totPop*100)

# Male population of a county as a percentage of total male population
census['M Pop as % of total M Pop'] = census.TOT_MALE.apply(lambda row: row/totM*100)

# Female population of a county as a percentage of total population
census['F Pop as % of total Pop'] = census.TOT_FEMALE.apply(lambda row: row/totPop*100)

# Female population of a county as a percentage of total female population
census['F Pop as % of total F Pop'] = census.TOT_FEMALE.apply(lambda row: row/totF*100)

# Hispanic population as a percentage of total population
census['H Pop as % of total Pop'] = census.TOT_H.apply(lambda row: row/totPop*100)

# White population as a percentage of total population
census['WA Pop as % of total Pop'] = census.TOT_WA.apply(lambda row: row/totPop*100)

# Black population as a percentage of total population
census['BA Pop as % of total Pop'] = census.TOT_BA.apply(lambda row: row/totPop*100)

# Asian population as a percentage of total population
census['AA Pop as % of total Pop'] = census.TOT_AA.apply(lambda row: row/totPop*100)

# Population of other races as a percentage of total population
census['Other Pop as % of total Pop'] = Other.apply(lambda row: row/totPop*100)

# Hispanic population 18+ as a percentage of total population 18+
census['H Pop as % of total Pop 18+'] = census['TOT_H_18+'].apply(lambda row: row/totPop18*100)

# White population 18+ as a percentage of total population 18+
census['WA Pop as % of total Pop 18+'] = census['TOT_WA_18+'].apply(lambda row: row/totPop18*100)

# Black population 18+ as a percentage of total population 18+
census['BA Pop as % of total Pop 18+'] = census['TOT_BA_18+'].apply(lambda row: row/totPop18*100)

# Asian population 18+ as a percentage of total population 18+
census['AA Pop as % of total Pop 18+'] = census['TOT_AA_18+'].apply(lambda row: row/totPop18*100)

# Population of other races 18+ as a percentage of total population 18+
census['Other Pop as % of total Pop 18+'] = Other18.apply(lambda row: row/totPop18*100)

# Percentage of occupied housing units by total housing units in Florida
census['% OCC TOTAL'] = census.OCC_HOUS_UNITS.apply(lambda row: row/totHous*100)


# In[21]:

# Create additional features by total population of a predictor in a county:

# Male population of a county as a percentage of total population in a county
census['M Pop as % of total Pop COUNTY'] = census.TOT_MALE.div(census.TOT_POP, axis='index')*100

# Female population of a county as a percentage of total population in a county
census['F Pop as % of total Pop COUNTY'] = census.TOT_FEMALE.div(census.TOT_POP, axis='index')*100

# Hispanic population as a percentage of total population in a county
census['H Pop as % of total Pop COUNTY'] = census.TOT_H.div(census.TOT_POP, axis='index')*100

# White population as a percentage of total population in a county
census['WA Pop as % of total Pop COUNTY'] = census.TOT_WA.div(census.TOT_POP, axis='index')*100

# Black population as a percentage of total population in a county
census['BA Pop as % of total Pop COUNTY'] = census.TOT_BA.div(census.TOT_POP, axis='index')*100

# Asian population as a percentage of total population in a county
census['AA Pop as % of total Pop COUNTY'] = census.TOT_AA.div(census.TOT_POP, axis='index')*100

# Population of other races as a percentage of total population in a county
census['Other Pop as % of total Pop COUNTY'] = Other.div(census.TOT_POP, axis='index')*100

# Hispanic population 18+ as a percentage of total population 18+ in a county
census['H Pop as % of total Pop 18+ COUNTY'] = census['TOT_H_18+'].div(census['TOT_18+'], axis='index')*100

# White population 18+ as a percentage of total population 18+ in a county
census['WA Pop as % of total Pop 18+ COUNTY'] = census['TOT_WA_18+'].div(census['TOT_18+'], axis='index')*100

# Black population 18+ as a percentage of total population 18+ in a county
census['BA Pop as % of total Pop 18+ COUNTY'] = census['TOT_BA_18+'].div(census['TOT_18+'], axis='index')*100

# Asian population 18+ as a percentage of total population 18+ in a county
census['AA Pop as % of total Pop 18+ COUNTY'] = census['TOT_AA_18+'].div(census['TOT_18+'], axis='index')*100

# Population of other races 18+ as a percentage of total population 18+ in a county
census['Other Pop as % of total Pop 18+ COUNTY'] = Other18.div(census['TOT_18+'], axis='index')*100

# Perncentage of occupied housing units by total housing units in a county
census['% OCC COUNTY'] = census.OCC_HOUS_UNITS.div(census.TOT_HOUS_UNITS, axis='index')*100


# In[22]:

# Write the census dataframe to CSV file
census.to_csv('FL_census.csv')

