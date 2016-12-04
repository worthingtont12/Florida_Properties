"""Clean up the data to make it easier to understand and use."""
import pandas as pd
import numpy as np
import re
# import smtplib
# from login_info import username, password, recipient1, recipient2, recipient3
# Loading Data
df = pd.read_stata('/Volumes/Seagate Backup Plus Drive/NAL/NAL2014/nal23rts2014.dta',
                   convert_categoricals=False)

# #############Functions#####################


def notna(obs):
    """Returns True if the value is not missing and returns False if it is missing.
    Logic is reversed for use cases below.
    arguments:
        obs:The observation of interest.
    """
    if np.isnan(obs) == False:
        return True
    else:
        return False


def in_range(obs, range_start, range_end):
    """Returns True if observation is in range specified.
    arguments:
        obs:The observation of interest.
        range_start:Start of range.Range is zero indexed.
        range_end:End of range.Range is zero indexed.
    """
    if obs in range(range_start, range_end):
        return True
    else:
        return False


##############Relabeling Levels#############
# redefining use codes to descriptive code
df['landuse'].astype('category')
map_landuse = {0: "Vacant Residential", 1: "Single Family", 2: "Mobile Homes", 3: "Multi-family - 10 units or more",
               4: "Condominiums", 5: "Cooperatives", 6: "Retirement Homes not eligible for exemption.", 7: "Miscellaneous Residential (migrant camps, boarding homes, etc.)",
               8: "Multi-family - less than 10 units", 9: "Undefined - Reserved for Use by Department of Revenue", 10: "Vacant Commercial", 11: "Stores, one story",
               12: "Mixed use - store and office or store and residential or residential combination", 13: "Department Stores", 14: "Supermarkets",
               15: "Regional Shopping Centers", 16: "Community Shopping Centers", 17: "Office buildings, non-professional service buildings, one story", 18: "Office buildings, non-professional service buildings, multi-story",
               19: "Professional service buildings", 20: "Airports (private or commercial), bus terminals, marine terminals, piers, marinas.", 21: "Restaurants, cafeterias",
               22: "Drive-in Restaurants", 23: "Financial institutions (banks, saving and loan companies, mortgage companies, credit services)", 24: "Insurance company offices",
               25: "Repair service shops (excluding automotive), radio and T.V. repair, refrigeration service, electric repair, laundries, laundromats", 26: "Service stations",
               27: "Auto sales, auto repair and storage, auto service shops, body and fender shops, commercial garages, farm and machinery sales and services, auto rental, marine equipment, trailers and related equipment, mobile home sales, motorcycles, construction vehicle sales",
               28: "Parking lots (commercial or patron) mobile home parks", 29: "Wholesale outlets, produce houses, manufacturing outlets", 30: "Florist, greenhouses",
               31: "Drive-in theaters, open stadiums", 32: "Enclosed theaters, enclosed auditoriums", 33: "Nightclubs, cocktail lounges, bars", 34: "Bowling alleys, skating rinks, pool halls, enclosed arenas",
               35: "Tourist attractions, permanent exhibits, other entertainment facilities, fairgrounds (privately owned).", 36: "Camps", 37: "Race tracks; horse, auto or dog",
               38: "Golf courses, driving ranges", 39: "Hotels, motels", 40: "Vacant Industrial", 41: "Light manufacturing, small equipment manufacturing plants, small machine shops, instrument manufacturing printing plants",
               42: "Heavy industrial, heavy equipment manufacturing, large machine shops, foundries, steel fabricating plants, auto or aircraft plants", 43: "Lumber yards, sawmills, planing mills",
               44: "Packing plants, fruit and vegetable packing plants, meat packing plants", 45: "Canneries, fruit and vegetable, bottlers and brewers distilleries, wineries", 46: "Other food processing, candy factories, bakeries, potato chip factories",
               47: "Mineral processing, phosphate processing, cement plants, refineries, clay plants, rock and gravel plants.", 48: "Warehousing, distribution terminals, trucking terminals, van and storage warehousing",
               49: "Open storage, new and used building supplies, junk yards, auto wrecking, fuel storage, equipment and material storage", 50: "Improved agricultural", 51: "Cropland soil capability Class I",
               52: "Cropland soil capability Class II", 53: "Cropland soil capability Class III", 54: "Timberland - site index 90 and above", 55: "Timberland - site index 80 to 89 056 Timberland - site index 70 to 79 057 Timberland - site index 60 to 69",
               58: "Timberland - site index 50 to 59 059 Timberland not classified by site index to Pines", 60: "Grazing land soil capability Class I", 61: "Grazing land soil capability Class II", 62: "Grazing land soil capability Class III",
               63: "Grazing land soil capability Class IV", 64: "Grazing land soil capability Class V", 65: "Grazing land soil capability Class VI", 66: "Orchard Groves, Citrus, etc.", 67: "Poultry, bees, tropical fish, rabbits, etc.",
               68: "Dairies, feed lots", 69: "Ornamentals, miscellaneous agricultural", 70: "Vacant , with or without extra features", 71: "Churches", 72: "Private schools and colleges", 73: "Privately owned hospitals",
               74: "Homes for the aged", 75: "Orphanages, other non-profit or charitable services", 76: "Mortuaries, cemeteries, crematoriums", 77: "Clubs, lodges, union halls", 78: "Sanitariums, convalescent and rest homes",
               79: "Cultural organizations, facilities", 80: "Undefined - Reserved for future use", 81: "Military", 82: "Forest, parks, recreational areas", 83: "Public county schools - include all property of Board of Public Instruction",
               84: "Colleges", 85: "Hospitals", 86: "Counties (other than public schools, colleges, hospitals) including non-municipal government.", 87: "State, other than military, forests, parks, recreational areas, colleges, hospitals",
               88: "Federal, other than military, forests, parks, recreational areas, hospitals, colleges", 89: "Municipal, other than parks, recreational areas, colleges, hospitals", 90: "Leasehold interests (government owned property leased by a non-governmental lessee)",
               91: "Utility, gas and electricity, telephone and telegraph, locally assessed railroads, water and sewer service, pipelines, canals, radio/television communication", 92: "Mining lands, petroleum lands, or gas lands", 93: "Subsurface rights",
               94: "Right-of-way, streets, roads, irrigation channel, ditch, etc.", 95: "Rivers and lakes, submerged lands", 96: "Sewage disposal, solid waste, borrow pits, drainage reservoirs, waste land, marsh, sand dunes, swamps",
               97: "Outdoor recreational or parkland, or high-water recharge subject to classified use assessment.", 98: "Centrally assessed Non-Agricultural Acreage Property", 99: "Acreage not zoned agricultural with or without extra features"}

df["landuse_explained"] = df["landuse"].map(map_landuse)

# subsetting for observation for when a sale was made in 2014
dfTest = df[~pd.isnull(df.sale_prc1)]
dfTest = dfTest[dfTest.sale_yr1 == 2014]

# if all obs are missing drop column
dfTest = dfTest.dropna(axis=1, how='all').copy()

# #############Feature Creation#############
# number of years since sale
dfTest.years_since_last_sale = (dfTest.sale_yr1.astype('float') - dfTest.sale_yr2.astype('float'))

# dummy varible for if sold before
dfTest.sold_before = dfTest.eff_yr_blt.apply(notna)

# Effective age of property
dfTest.eff_age = (dfTest.sale_yr1.astype('float') - dfTest.eff_yr_blt.astype('float'))

# Actual age of property
dfTest.act_age = (dfTest.sale_yr1.astype('float') - dfTest.act_yr_blt.astype('float'))

# recoding landuse to dummy variables
dfTest.landuse = dfTest.landuse.astype(int)
# type = residential
dfTest.residential = dfTest.landuse.apply(lambda row: in_range(row, 0, 10))

# type = commercial
dfTest.commercial = dfTest.landuse.apply(lambda row: in_range(row, 10, 40))

# type = industrial
dfTest.industrial = dfTest.landuse.apply(lambda row: in_range(row, 40, 50))

# type = agricultural
dfTest.agricultural = dfTest.landuse.apply(lambda row: in_range(row, 50, 70))

# type = institutional
dfTest.institutional = dfTest.landuse.apply(lambda row: in_range(row, 70, 80))

# type = government
dfTest.government = dfTest.landuse.apply(lambda row: in_range(row, 80, 90))

# type = miscellaneous
dfTest.miscellaneous = dfTest.landuse.apply(lambda row: in_range(row, 90, 97))

# type = Centrally Assessed Property
dfTest.cap = dfTest.landuse.apply(lambda row: in_range(row, 98, 99))

# type = Non-Agricultural Acreage Property
dfTest.naap = dfTest.landuse.apply(lambda row: in_range(row, 99, 100))

# difference between sale price and just value
dfTest.diff_btwn_prc_jv = (dfTest.sale_prc1 - dfTest.jv)
dfTest.diff_pct = ((dfTest.diff_btwn_prc_jv / dfTest.jv) * 100)

# number of days since last sale
#
# # Email when finished
# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.starttls()
#
# server.login(username, password)
#
# server.sendmail(username, recipient1, 'Case study script is done')
# server.sendmail(username, recipient2, 'Case study script is done')
# server.sendmail(username, recipient3, 'Case study script is done')
dfTest.to_csv('miami_cleaned.csv')
