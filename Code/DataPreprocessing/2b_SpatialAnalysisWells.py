# === WELL SPATIAL ANALYSIS CODE ===
# Written by Danielle Tadych

# The purpose of this script is to create a code to spatially analyze all the wells in 
# the combined database based on management. 

# WORKFLOW
# 1. Read in the master ADWR database static database, water level database, and 
#       georegions shapefile created in QGIS
# 2. Overlay region shapefile on static well database shapefile
# 3. Export a dataframe (registry list) of combined ID's with the columns we want 
#       (regulation, etc.)
# 4. Join the registry list with the timeseries database so every well has water 
#       levels and is tagged with a category we want
# 5. Create pivot tables averaging water levels based on categories (e.g. regulation, 
#       access to SW, or georegion (finer scale))
# 6. Export pivot tables into .csv's for easy analyzing later
#       * Note: after reading in packages, skip to line 233 to avoid redoing steps 1-5
#         or to read in the web .csv's

# %%
import os
import numpy as np
import pandas as pd
import geopandas as gp

# Local paths

inputpath = '../../Data/Input'
shapepath = '../../Data/Input/Shapefiles'
outputpath = '../../Data/Output/Local'

# %%
# Load in the master databases (Takes about 5 mins)
filename_mdb_nd = 'Master_ADWR_database_noduplicates.shp'
filepath = os.path.join(outputpath, filename_mdb_nd)
print(filepath)

masterdb = gp.read_file(filepath)
pd.options.display.float_format = '{:.2f}'.format
print(masterdb.info())

# %%
# Reading in the shapefile
filename_georeg = 'georeg_reproject_fixed.shp'
filepath = os.path.join(shapepath, filename_georeg)
georeg = gp.read_file(filepath)
georeg.plot(cmap='viridis')

#%%
georeg['GEOREGI_NU'] = georeg['GEOREGI_NU'].astype('int64')
georeg.info()

# %% Overlay georegions onto the static database
# Going to use sjoin based off this website: https://geopandas.org/docs/user_guide/mergingdata.html
print("Non-cancelled: ", masterdb.crs, "Georegions: ", georeg.crs)

# %%
georeg = georeg.to_crs(epsg=26912)
masterdb2 = masterdb.set_crs(epsg=26912)
# %% Merge (~ 40s)
static_geo = gp.sjoin(masterdb2, georeg, how="inner", predicate='intersects')
static_geo.head()
print(str(filename_mdb_nd) + " and " + str(filename_georeg) + " join complete.")

# %% Exporting or reading in the static geodatabase instead of rerunning
static_geo.to_csv(outputpath+'/Final_Static_geodatabase_allwells.csv')

# %%
filename = "Final_Static_geodatabase_allwells.csv"
filepath = os.path.join(outputpath, filename)
static_geo = pd.read_csv(filepath)
static_geo

# %% Create a dataframe of Final_Region and Well ID's
reg_list = static_geo[['Combo_ID', 'GEO_Region', 'GEOREGI_NU','Water_CAT', 'Loc','Regulation','WELL_DEPTH','WELL_TYPE_']]
reg_list

# %% Converting Combo_ID to int
reg_list['Combo_ID'] = reg_list['Combo_ID'].astype(np.int64, errors = 'raise')

#%%
# Read in the annual time series database
filename_ts = 'Wells55_GWSI_WLTS_DB_annual_updated_thresh15outliersdeleted.csv'
filepath = os.path.join(outputpath, filename_ts)
print(filepath)
annual_db = pd.read_csv(filepath, header=1, index_col=0)
annual_db

# %%
annual_db = annual_db[1:168102]
annual_db
# %%
annual_db.index = annual_db.index.astype('int64')
# %%
annual_db2 = annual_db.reset_index(inplace=True)
annual_db2 = annual_db.rename(columns = {'year':'Combo_ID'})
annual_db2.head()

# %% Add list to the annual database
combo = annual_db2.merge(reg_list, how="inner")
combo.info()

# %% set index to Combo_ID
combo.set_index('Combo_ID', inplace=True)

# %% Sort the values
combo = combo.sort_values(by=['GEOREGI_NU'])
combo

# %%
combo_forsw = combo.copy()
combo_forsw = combo_forsw.drop(['GEO_Region','Loc','Regulation','WELL_DEPTH','WELL_TYPE_'],axis=1)
# combo_new

combo_forreg = combo.copy()
combo_forreg = combo_forreg.drop(['GEO_Region','Loc','Water_CAT','WELL_DEPTH','WELL_TYPE_'],axis=1)
combo_forreg
# %% This is to adjust categories as desired
# combo_new.loc[combo_new['Water_CAT']=='No_CAP', 'Water_CAT'] = 'NoSurf'
# combo_new.loc[combo_new['Water_CAT']=='GW', 'Water_CAT'] = 'NoSurf'
# combo_new.loc[combo_new['Water_CAT']=='Mix', 'Water_CAT'] = 'NoSurf'
# combo_new.loc[combo_new['Water_CAT']=='SW', 'Water_CAT'] = 'SWapp'
# combo_new.loc[combo_new['Water_CAT']=='CAP', 'Water_CAT'] = 'SWapp'
combo_forsw['Water_CAT'].unique()

# %% Now for aggregating by category for the timeseries (Spatial Average)
cat_wl_reg = combo_forreg.groupby(['Regulation']).mean()
cat_wl_SW = combo_forsw.groupby(['Water_CAT']).mean()

cat_wl_SW

# %% 
cat_wl2_reg = cat_wl_reg.copy()
cat_wl2_SW = cat_wl_SW.copy()

# Clean up the dataframe for graphing
        
i = cat_wl2_reg
del i['GEOREGI_NU']
# del i['WELL_DEPTH']
f = i.transpose()
f.reset_index(inplace=True)
f['index'] = pd.to_numeric(f['index'])
f['index'] = f['index'].astype(int)
f.set_index('index', inplace=True)
f.info()
cat_wl2_reg = f

i = cat_wl2_SW
del i['GEOREGI_NU']
# del i['WELL_DEPTH']
f = i.transpose()
f.reset_index(inplace=True)
f['index'] = pd.to_numeric(f['index'])
f['index'] = f['index'].astype(int)
f.set_index('index', inplace=True)
f.info()
cat_wl2_SW = f

# %% Going to export all these as CSV's
cat_wl2_reg.to_csv(outputpath+'/Waterlevels_Regulation_updated_thresh15outliersdeleted.csv')
cat_wl2_SW.to_csv(outputpath+'/Waterlevels_AccesstoSW_updated_thresh15outliersdeleted.csv')
# %%
