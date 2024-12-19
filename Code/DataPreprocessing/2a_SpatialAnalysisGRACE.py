# === GRACE Spatial Analysis Script ===
# written by Danielle Tadych

# The purpose of this script is to analyze GRACE Data for Arizona by points and shapes
#  - Importing packages: Line 8
#  - Reading in files: Line 19
#  - Calculating the average based off a mask (not weighted): Line 73
# %%
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gp
import xarray as xr
import netCDF4

print("Packages Loaded.")

# %% Read in the file
filename = 'CSR_GRACE_GRACE-FO_RL0602_Mascons_all-corrections.nc'
datapath = '../../Data/Input/'
outputpath = '../../Data/Output/Local/'
shapepath = '../../Data/Input/Shapefiles/'

grace_dataset = xr.open_dataset(datapath+'/'+filename)
grace_dataset

# %% Read in the mask shapefiles
filename_georeg = 'georeg_reproject_fixed.shp'
filepath = os.path.join(shapepath, filename_georeg)
georeg = gp.read_file(filepath)
georeg.plot()

# %% View first 5 values
grace_dataset["lwe_thickness"]["lat"].values[:5]
print("The min and max latitude values in the data is:", 
      grace_dataset["lwe_thickness"]["lat"].values.min(), 
      grace_dataset["lwe_thickness"]["lat"].values.max())
print("The min and max longitude values in the data is:", 
      grace_dataset["lwe_thickness"]["lon"].values.min(), 
      grace_dataset["lwe_thickness"]["lon"].values.max())

print("The earliest date in the data is:", 
    grace_dataset["lwe_thickness"]["time"].values.min())
print("The latest date in the data is:", 
    grace_dataset["lwe_thickness"]["time"].values.max())

# %%
print("Number of Datapoints")
grace_dataset["lwe_thickness"]['time'].values.shape   

# %% Slicing data to get variables
lat = grace_dataset.variables['lat'][:]
lon = grace_dataset.variables['lon'][:]
time = grace_dataset.variables['time'][:]
lwe = grace_dataset['lwe_thickness']
lwe

# %% Now I need to assign a coordinate system to lwe
lwe.coords['lon'] = (lwe.coords['lon'] + 180) % 360 - 180
lwe2 = lwe.sortby(lwe.lon)
lwe2 = lwe2.rio.set_spatial_dims('lon', 'lat')
lwe2 = lwe2.rio.set_crs("epsg:4269")
lwe2.rio.crs

# %% Convert time to datetime format
time = grace_dataset.variables['time'] # do not cast to numpy array yet 
time_convert = netCDF4.num2date(time[:], "days since 2002-01-01T00:00:00Z", calendar='standard')
lwe2['time'] = time_convert
datetimeindex = lwe2.indexes['time'].to_datetimeindex()
lwe2['time'] = datetimeindex

# %%
# ---- Creating Averages Based off Shape File Mask ----
# Check the cooridnate systems
mask = georeg

# print("mask crs:", counties.crs)
print("mask crs: ",mask.crs)
print("data crs:", lwe2.rio.crs)

# %% Change the coordinate system if needed
mask = mask.to_crs(4269)
mask.crs

# %% Clipping based off the mask (not weighted)
clipped = lwe2.rio.clip(mask.geometry, mask.crs)
print("Clipping finished.")
# %% Checking to see if it clipped correctly
fig, ax = plt.subplots(figsize=(6, 6))
clipped[0,:,:].plot()
mask.boundary.plot(ax=ax)
ax.set_title("Shapefile Clip Extent",
             fontsize=16)
plt.show()

# %%
clipped['time'] = datetimeindex
clipped_mean = clipped.mean(("lon","lat"))
clipped_mean
cm_df = pd.DataFrame(clipped_mean)
cm_df = cm_df.reset_index()
cm_df['index'] = datetimeindex
cm_df.set_index('index', inplace=True)
cm_df

# %%
# Extract the year from the date column and create a new column year
cm_df['year'] = pd.DatetimeIndex(cm_df.index).year
cm_df_year = pd.pivot_table(cm_df, index=["year"], values=[0], dropna=False, aggfunc=np.mean)
cm_df_year

cm_df_year.plot() # Test Plot
# %% Write the csv
cm_df_year.to_csv(outputpath+'grace_stateavg_yearly.csv')