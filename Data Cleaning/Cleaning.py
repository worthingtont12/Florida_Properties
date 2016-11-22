"""Clean up the data to make it easier to understand and use."""
import pandas as pd
#Loading Data
df = pd.read_stata('/Volumes/Seagate Backup Plus Drive/NAL/NAL2014/nal23rts2014.dta', convert_categoricals=False)

#relabeling levels
#use codes
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
#recoding landuse to dummy variables

# Compute mean for census block 'Just Value' and add as column in dataframe; currently mean is based off properties in CB WITH
# same landuse code
dfTest['Blk_Val'] = dfTest_cb.groupby([dfTest_cb['census_bk'], dfTest_cb['landuse']])['jv'].transform('mean')

# Compute season-of-sale
dfTest['sale_mo1'].astype('category')
map_landuse = {1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring", 6: "Summer", 7: "Summer",
8: "Summer", 9: "Fall", 10: "Fall", 11: "Fall", 12: "Winter" }
dfTest["sale_season1"] = dfTest["sale_mo1"].map(map_landuse)
