import pandas as pd
# df = pd.read_stata('/Volumes/Seagate Backup Plus Drive/NAL/NAL2014/nal11rts2014.dta')
# print(df.columns.values)

#Import all data files for the year
fulldf = pd.DataFrame()
listdf = []
for i in range(11, 78):
    df = pd.read_stata('/Volumes/Seagate Backup Plus Drive/NAL/NAL2014/nal'+str(i)+'rts2014.dta',convert_categoricals=False, convert_missing=True)
    df['County_Code'] = i
    listdf.append(df)

fulldf = pd.concat(listdf)
