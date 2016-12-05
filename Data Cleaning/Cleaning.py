"""Clean up the data to make it easier to understand and use."""
import pandas as pd
import numpy as np
from FL_Census_Tract import census
# import smtplib
# from login_info import username, password, recipient1, recipient2, recipient3
# Loading Data
# Import all years
listdf = []
for i in range(11, 78):
    dftmp = pd.read_stata("/Volumes/Tyler's External Hard Drive/NAL2014/nal" +
                          str(i) + "rts2014.dta", convert_categoricals=False, convert_missing=True)
    dftmp['County_Code'] = i
    listdf.append(dftmp)
yeardf = pd.concat(listdf)

df = yeardf
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


def remove_last_character(string, number):
    """Takes in a string and removes the last x characters.
    Parameters
    ----------
    string : A string.
    number : Number of characters to be removed.
    """
    string = string
    string = string[:-number]
    return string


# #############Relabeling Levels#############
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

# redefining Construction Class
df['const_class'].astype('category')
map_class = {1.0: 'Fireproof Steel', 2.0: 'Reinforced Concrete', 3.0: 'Masonry',
             4.0: 'Wood (include steal studs)', 5.0: 'Steel Frame/incombustible walls/roof'}
df['const_class_explained'] = df['const_class'].map(map_class)

# redefining Vacant / Improved Code
df['vi_cd1'] = df['vi_cd1'].astype('category')
map_vi = {'V': 'Vacant land', 'I': 'Improved property'}
df['vi_cd1_explained'] = df['vi_cd1'].map(map_vi)

# refining Fiduciary Code
df['fidu_cd'] = df['fidu_cd'].astype('category')
map_fc = {1: 'Personal representative', 2: 'Financial institution', 3: 'Other'}
df['fidu_cd_explained'] = df['fidu_cd'].map(map_fc)

# Compute season-of-sale
df['sale_mo1'] = df['sale_mo1'].astype('category')
map_season = {1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring", 6: "Summer", 7: "Summer",
              8: "Summer", 9: "Fall", 10: "Fall", 11: "Fall", 12: "Winter"}
df["sale_season1"] = df["sale_mo1"].map(map_season)

# subsetting for observation for when a sale was made in 2014
dfTest = df[~pd.isnull(df.sale_prc1)]
dfTest = dfTest[dfTest.sale_yr1 == 2014]

# if all obs are missing drop column
dfTest = dfTest.dropna(axis=1, how='all').copy()

# #############Feature Creation#############

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

# Deleting '100's from Sales Price 1
dfTest.sale_prc1 = dfTest.sale_prc1.replace('100', np.nan)

# difference between sale price and just value
dfTest.diff_btwn_prc_jv = (dfTest.sale_prc1 - dfTest.jv)
dfTest.diff_pct = ((dfTest.diff_btwn_prc_jv / dfTest.jv) * 100)

# Compute mean for census block 'Just Value' and add as column in dataframe; currently mean is based off properties in CB WITH
# same landuse code
dfTest['Blk_Val'] = dfTest.groupby([dfTest['census_bk'], dfTest['landuse']])[
    'jv'].transform('mean')

# Drop unnecessary columns
dfTest = dfTest.drop(["app_stat", "ass_dif_trns", "ass_trnsfr_fg", "atv_strt", "av_class_use", "av_consrv_lnd", "av_hmstd",
                      "av_non_hmstd_resd", "av_nsd", "av_resd_non_resd", "av_sd", "co_app_stat", "cono_prv_hm", "del_val", "distr_cd", "distr_yr", "exmpt_01",
                      "exmpt_02", "exmpt_03", "exmpt_05", "exmpt_07", "exmpt_08", "exmpt_09", "exmpt_15", "exmpt_16", "exmpt_17", "exmpt_18", "exmpt_20",
                      "exmpt_26", "exmpt_31", "exmpt_32", "exmpt_33", "exmpt_34", "exmpt_35", "exmpt_39", "exmpt_80", "exmpt_81", "file_t", "grp_no", "jv_chng",
                      "jv_chng_cd", "jv_class_use", "jv_consrv_lnd", "jv_hmstd", "jv_non_hmstd_resd", "jv_resd_non_resd", "multi_par_sal2",
                      "nconst_val", "or_book1", "or_book2", "or_page1", "or_page2", "own_addr1", "own_addr2", "own_city", "own_name", "own_state", "own_zipcd",
                      "par_splt", "parcel", "parcel_id_prv_hmstd", "parcel_orig", "prev_hmstd_own", "qual_cd1", "qual_cd2", "rng", "rng_orig", "rs_id",
                      "s_legal", "sec", "sec_orig", "seq_no", "tax_auth_cd", "taxauthc", "tv_nsd", "tv_sd",
                      "twn", "twn_orig", "vi_cd2", "yr_val_trnsf"], axis=1)

# Creating Census Tract for Merging
dfTest['census_tract'] = dfTest['census_bk'].astype('float').astype(
    'str').apply(lambda row: remove_last_character(row, 3))

# Merging dfs
dfTest2 = pd.merge(dfTest, census, on="census_tract")

print(dfTest.head(5))

# email when done
# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.starttls()
#
# server.login(username, password)
#
# server.sendmail(username, recipient1, 'Case study script is done')
# server.sendmail(username, recipient2, 'Case study script is done')
# server.sendmail(username, recipient3, 'Case study script is done')


dfTest.to_csv('florida_cleaned.csv')
