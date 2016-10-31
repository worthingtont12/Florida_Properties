import pandas as pd
#Import all data files for the year
fulldf = pd.DataFrame()
yeardf = []
for i in range(11, 78):
    df = pd.read_stata('/Volumes/Seagate Backup Plus Drive/NAL/NAL2014/nal'+str(i)+'rts2014.dta',convert_categoricals=False, convert_missing=True)
    df['County_Code'] = i
    yeardf.append(df)
#
# fulldf = pd.concat(listdf)
# #Import all years
# for j in range(1995, 2014):
#     for i in range(11, 78):
#         df = pd.read_stata('/Volumes/Seagate Backup Plus Drive/NAL/NAL'+str(j)+'/nal'+str(i)+'rts2014.dta',convert_categoricals=False, convert_missing=True)
#         df['County_Code'] = i
#         df['File_Year'] = j
#         listdf.append(df)
#
# fulldf = pd.concat(listdf)
