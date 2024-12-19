# ----- All Paper Graphs except graphics from QGIS -----
# %% Load the packages
from cProfile import label
from operator import ge
from optparse import Values
import os
from geopandas.tools.sjoin import sjoin
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import ListedColormap
import datetime
from matplotlib.transforms import Bbox
import seaborn as sns
import numpy as np
import pandas as pd
from shapely.geometry import box
import geopandas as gp
import scipy.stats as sp
from scipy.stats import kendalltau, pearsonr, spearmanr
import pymannkendall as mk
import Customfunctions

# === Assign Data paths ===

# This is if you created your own database
datapath_local = '../Data'
inputpath_local = '../Data/Input_files/'
outputpath_local = '../Data/Output_files/'
figurepath = '../Data/Figures/'

datapath = '../../Data/Input/'
shapedir = '../../Data/Input/Shapefiles/'
outputpath = '../../Data/Output/Local/'

# %% Read in the data

# Importing Water Level Values
# For statewide
filename_ts = 'Wells55_GWSI_WLTS_DB_annual.csv'
filepath = os.path.join(datapath, filename_ts)
# filename_ts = 'Wells55_GWSI_WLTS_DB_annual_updated_thresh15outliersdeleted.csv'
# filepath = os.path.join(outputpath, filename_ts)
print(filepath)
annual_db = pd.read_csv(filepath, header=1, index_col=0)
annual_db.head()

# For regulation
filepath = outputpath+'/Waterlevels_Regulation_updated_thresh15.csv'
# filepath = outputpath+'/Waterlevels_Regulation_updated_MAX.csv'
# filepath = outputpath+'/Waterlevels_Regulation_updated_MIN.csv'
cat_wl2_reg = pd.read_csv(filepath, index_col=0)
cat_wl2_reg.head()

# For Access to SW
filepath = outputpath+'/Waterlevels_AccesstoSW_updated_thresh15.csv'
# filepath = outputpath+'/Waterlevels_AccesstoSW_updated_MAX.csv'
# filepath = outputpath+'/Waterlevels_AccesstoSW_updated_MIN.csv'
cat_wl2_SW = pd.read_csv(filepath, index_col=0)
cat_wl2_SW.head()

# %% Importing GRACE analyses
filepath = filepath = outputpath+'grace_stateavg_yearly.csv'
# filepath = outputpath_local+'gracse_remapped_yearly.csv'
grace_yearly = pd.read_csv(filepath, index_col=0)
grace_yearly = grace_yearly[:-1]

# Reading in the shapefile - note, figure 2 is created through QGIS
filename_georeg = 'georeg_reproject_fixed.shp'
filepath = os.path.join(shapedir, filename_georeg)

# %% Read in the drought indices file
drought_indices = pd.read_csv(inputpath_local+'Yearly_DroughtIndices_updated12032023.csv') #this version doesn't have PHDI so adjust accordingly
drought_indices = drought_indices.set_index('In_year')


# %% Creating colors
# Matching map
cap = '#C6652B'
# noCAP = '#EDE461' # This is one from the map but it's too bright and hard to see
noCAP = '#CCC339' # This color but darker for lines
GWdom = '#3B76AF'
mixed = '#6EB2E4'
swdom = '#469B76'
specialyears = 'darkgray'

drought_color = '#ffa6b8'
wet_color = '#b8d3f2'

grace_color = '#858585'
state_color = 'black'

# %% Figure 3
minyear = 1975
maxyear = 2022
fsize = 14

fig, ax = plt.subplots(2, 1, figsize=(9, 10))

# Plot for the first graph
ax[0].plot(drought_indices['PHDI'], label='PHDI', lw=3)
ax[0].plot(drought_indices['PDSI'], label='PDSI', lw=2)
ax[0].plot(drought_indices['dry'], '-.', label='Cutoff Value', color='black', zorder=5)

# Drought Year Shading
drought_years = [(1988, 1990), (1995, 1996), (2021, 2022), (2002, 2004), (2005, 2008), (2012, 2015), (2018, 2019)]
for start, end in drought_years:
    ax[0].axvspan(start, end, color=drought_color, alpha=0.5, lw=0, label="Severe Drought" if start == 1988 else "")

ax[0].set_xlim(minyear, maxyear)
ax[0].set_ylim(-6, 6)
# ax[0].grid(visible=True, which='major')
ax[0].grid(which='minor', color='#EEEEEE', lw=0.8)
# ax[0].set_xlabel('Year', fontsize=fsize)
ax[0].set_ylabel('Index Values', fontsize=fsize)
ax[0].legend(loc='best', fontsize=fsize)
ax[0].set_title('a)', fontsize=fsize, loc='left', pad=15)
ax[0].tick_params(axis='y', labelsize=fsize)
ax[0].tick_params(axis='x', labelsize=fsize, rotation=0)

# Data preparation for the second graph
adb_statemean = annual_db.mean()
adb_meandf = pd.DataFrame(adb_statemean)
# adb_meandf = adb_meandf.index.astype(int)
f = adb_meandf
f.reset_index(inplace=True)
f['index'] = pd.to_numeric(f['index'])
f['index'] = f['index'].astype(int)
f.set_index('index', inplace=True)

adb_meandf = f

ds = adb_meandf

betterlabels = ['State Average DTW'] 

f = ds[(ds.index >= minyear) & (ds.index <= maxyear)]
columns = ds.columns
column_list = ds.columns.tolist()

stats = pd.DataFrame()
for i in column_list:
        df = f[i]
        # df = f[i].pct_change()
        #print(df)
        y=np.array(df.values, dtype=float)
        x=np.array(pd.to_datetime(df).index.values, dtype=float)
        slope, intercept, r_value, p_value, std_err =sp.linregress(x,y)
        stats = stats._append({'slope': slope, 'int':intercept, 
                              'rsq':r_value*r_value, 'p_val':p_value, 
                              'std_err':std_err, 'mean': np.mean(y),
                              'var': np.var(y),'sum': np.sum(y)},
                              ignore_index=True)

stats.index = betterlabels
stats1 = stats.transpose()
print(stats1)
# # -- Data visualization --
xf = np.linspace(min(x),max(x),100)
xf1 = xf.copy()
m1 = round(stats1.loc['slope',betterlabels[0]], 2)
yint1 = round(stats1.loc['int',betterlabels[0]], 2)
rsq1 = round(stats1.loc['rsq', betterlabels[0]], 4)
pval1 = round(stats1.loc['p_val', betterlabels[0]], 4)
yf1 = (m1*xf)+yint1

ax[1].plot(xf1, yf1,"-.",color=state_color, lw=1)
ax[1].plot(ds.index, ds, label='Arizona Average DTW', color='black', zorder=2)

# Add drought shading
for start, end in drought_years:
    ax[1].axvspan(start, end, color=drought_color, alpha=0.5, lw=0)

ax[1].set_xlim([minyear, maxyear])
ax[1].set_ylim(300, 75)
ax[1].set_xlabel('Year', fontsize=fsize)
ax[1].set_ylabel('Depth to Water (ft)', fontsize=fsize)
ax[1].set_title('b)', fontsize=fsize, loc='left', pad=15)

# Secondary axis for GRACE data
ax2 = ax[1].twinx()
ax2.plot(grace_yearly.index, grace_yearly['0'], label='State Average LWE', color='#858585', zorder=1, lw=2)
ax2.set_ylim([-15, 15])
ax2.set_ylabel(u'Δ LWE (cm)', fontsize=14)

# Combine legends
lines, labels = ax[1].get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax[1].legend(lines + lines2, labels + labels2, loc='upper right', fontsize=fsize)

ax[1].tick_params(axis='y', labelsize=fsize)
ax2.tick_params(axis='y', labelsize=fsize)
ax[1].tick_params(axis='x', labelsize=fsize, rotation=0)

fig.set_dpi(600.0)
plt.savefig(figurepath + 'Figure 3', bbox_inches='tight')
plt.show()

# %% Figure 7a
# For Depth to Water by regulation
ds = cat_wl2_reg
min_yr = 2000
mx_yr = 2022
Name = "mean_Regulation"

del cat_wl2_reg['Res']
betterlabels = ['Regulated','Unregulated'] 

f = ds[(ds.index >= min_yr) & (ds.index <= mx_yr)]
columns = ds.columns
column_list = ds.columns.tolist()

stats = pd.DataFrame()
# for i in range(1, 12, 1):
for i in column_list:
        df = f[i]
        #print(df)
        y=np.array(df.values, dtype=float)
        x=np.array(pd.to_datetime(df).index.values, dtype=float)
        slope, intercept, r_value, p_value, std_err =sp.linregress(x,y)
        stats = stats._append({'slope': slope, 
                              'int':intercept, 
                              'rsq':r_value*r_value, 
                              'p_val':p_value, 
                              'std_err':std_err, 
                              'mean': np.mean(y),
                              'var': np.var(y),
                              'sum': np.sum(y)
                              },
                              ignore_index=True)


stats.index = betterlabels
stats1 = stats.transpose()
print(stats1)

# -- Data visualization --
xf = np.linspace(min(x),max(x),100)
xf1 = xf.copy()
#xf1 = pd.to_datetime(xf1)
m1 = round(stats1.loc['slope','Regulated'], 2)
m2 = round(stats1.loc['slope','Unregulated'], 2)
yint1 = round(stats1.loc['int','Regulated'], 2)
yint2 = round(stats1.loc['int','Unregulated'], 2)
pval1 = round(stats1.loc['p_val', 'Regulated'], 4)
pval2 = round(stats1.loc['p_val', 'Unregulated'], 4)

yf1 = (m1*xf)+yint1
yf2 = (m2*xf)+yint2

fig, ax = plt.subplots(1, 1, figsize = (8,5))

min_y = 75
max_y = 300
fsize = 12

# Drought Year Shading
a = 1988.5
b = 1990.5
c = 1995.5
d = 1996.5
e = 2020.5
f = 2021.5
g = 2001.5
h = 2003.5
i = 2005.5
j = 2007.5
k = 2011.5
l = 2014.5
m = 2017.5
n = 2018.5
plt.axvspan(a, b, color=drought_color, alpha=0.5, lw=0
            , label="Severe Drought"
            )
plt.axvspan(c, d, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(e, f, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(g, h, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(i, j, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(k, l, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(m, n, color=drought_color, alpha=0.5, lw=0)

ax.plot(ds['R'], label='Regulated', color=cap) 
ax.plot(ds['U'], label='Unregulated', color=GWdom) 

ax.plot(xf1, yf1,"-.",color='k',label='Linear Trendline', lw=1)
ax.plot(xf1, yf1,"-.",color=cap, lw=1)
ax.plot(xf1, yf2,"-.",color=GWdom, lw=1)

ax.set_xlim(min_yr,mx_yr)
ax.set_ylim(min_y,max_y)
# ax.grid(True)
ax.grid(visible=True,which='major')
ax.grid(which='minor',color='#EEEEEE', lw=0.8)
ax.set_xlabel('Year', fontsize=fsize)
ax.set_ylabel('Depth to Water (ft)',fontsize=fsize)
ax.minorticks_on()
fig.set_dpi(600.0)
# ax.set_title('a)',loc='left',pad=15)
ax.legend(loc='lower left')

#Putting Grace on a secondary axis
ax2 = ax.twinx()
ax2.plot(grace_yearly['0'], label='State Average LWE', color='k',zorder=1)
ax2.set_ylim([15, -15])
ax2.set_ylabel(u'Δ LWE (cm)',fontsize=fsize)
ax2.legend(loc='lower right')

plt.savefig(figurepath+Name, bbox_inches = 'tight')

# %% Figure 7c
# For Depth to Water by SW Access
ds = cat_wl2_SW
min_yr = 2000
mx_yr = 2022
Name = "Mean_A2SW"

del cat_wl2_SW['Res']

betterlabels = ['Recieves CAP'
                ,'GW Dominated (Regulated)'
                ,'Surface Water Dominated'
                ,'GW Dominated'
                ,'Mixed Source'] 

f = ds[(ds.index >= min_yr) & (ds.index <= mx_yr)]
columns = ds.columns
column_list = ds.columns.tolist()

stats = pd.DataFrame()
for i in column_list:
        df = f[i]
        # df = f[i].pct_change()
        #print(df)
        y=np.array(df.values, dtype=float)
        x=np.array(pd.to_datetime(df).index.values, dtype=float)
        slope, intercept, r_value, p_value, std_err =sp.linregress(x,y)
        stats = stats._append({'slope': slope, 'int':intercept, 
                              'rsq':r_value*r_value, 'p_val':p_value, 
                              'std_err':std_err, 'mean': np.mean(y),
                              'var': np.var(y),'sum': np.sum(y)},
                              ignore_index=True)

stats.index = betterlabels
stats1 = stats.transpose()
print(stats1)
# -- Data visualization --
xf = np.linspace(min(x),max(x),100)
xf1 = xf.copy()
m1 = round(stats1.loc['slope',betterlabels[0]], 2)
m2 = round(stats1.loc['slope',betterlabels[3]], 2)
m3 = round(stats1.loc['slope',betterlabels[4]], 2)
m4 = round(stats1.loc['slope',betterlabels[1]], 2)
m5 = round(stats1.loc['slope',betterlabels[2]], 2)
yint1 = round(stats1.loc['int',betterlabels[0]], 2)
yint2 = round(stats1.loc['int',betterlabels[3]], 2)
yint3 = round(stats1.loc['int',betterlabels[4]], 2)
yint4 = round(stats1.loc['int',betterlabels[1]], 2)
yint5 = round(stats1.loc['int',betterlabels[2]], 2)
rsq1 = round(stats1.loc['rsq', betterlabels[0]], 4)
rsq2 = round(stats1.loc['rsq', betterlabels[3]], 4)
rsq3 = round(stats1.loc['rsq', betterlabels[4]], 4)
rsq4 = round(stats1.loc['rsq', betterlabels[1]], 4)
rsq5 = round(stats1.loc['rsq', betterlabels[2]], 4)
pval1 = round(stats1.loc['p_val', betterlabels[0]], 4)
pval2 = round(stats1.loc['p_val', betterlabels[3]], 4)
pval3 = round(stats1.loc['p_val', betterlabels[4]], 4)
pval4 = round(stats1.loc['p_val', betterlabels[1]], 4)
pval5 = round(stats1.loc['p_val', betterlabels[2]], 4)
yf1 = (m1*xf)+yint1
yf2 = (m2*xf)+yint2
yf3 = (m3*xf)+yint3
yf4 = (m4*xf)+yint4
yf5 = (m5*xf)+yint5

fig, ax = plt.subplots(1, 1, figsize = (8,5))

# Drought Year Shading
a = 1988.5
b = 1990.5
c = 1995.5
d = 1996.5
# e = 1999.5
# f = 2000.5
g = 2001.5
h = 2003.5
i = 2005.5
j = 2007.5
k = 2011.5
l = 2014.5
m = 2017.5
n = 2018.5
plt.axvspan(a, b, color=drought_color, alpha=0.5, lw=0, label="Drought")
plt.axvspan(c, d, color=drought_color, alpha=0.5, lw=0)
# plt.axvspan(e, f, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(g, h, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(i, j, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(k, l, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(m, n, color=drought_color, alpha=0.5, lw=0)


ax.plot(xf1, yf1,"-.",color=cap, lw=1)
ax.plot(xf1, yf2,"-.",color=GWdom, lw=1)
ax.plot(xf1, yf3,"-.",color=mixed, lw=1)
ax.plot(xf1, yf4,"-.",color='#CCC339', lw=1)
ax.plot(xf1, yf5,"-.",color=swdom, lw=1)

min_y = 0
max_y = 400
fsize = 12

ax.plot(ds['CAP'], label=betterlabels[0], color=cap,zorder=2)
ax.plot(ds['No_CAP'], label=betterlabels[1], color='#CCC339',zorder=2) 
ax.plot(ds['SW'], label=betterlabels[2], color=swdom,zorder=2) 
ax.plot(ds['Mix'], label=betterlabels[4], color=mixed,zorder=2)
ax.plot(ds['GW'], label=betterlabels[3], color=GWdom,zorder=2)  

ax.set_xlim([min_yr,mx_yr])
ax.set_ylim(min_y,max_y)
# ax.grid(True)
ax.grid(visible=True,which='major')
ax.grid(which='minor',color='#EEEEEE', lw=0.8)
ax.set_xlabel('Year', fontsize=fsize)
ax.set_ylabel('Depth to Water (ft)',fontsize=fsize)
ax.minorticks_on()
fig.set_dpi(600.0)
# ax.set_title('c)',fontsize = fsize,loc='left',pad=15)
ax.legend(loc = [1.15,0.5])

#Putting Grace on a secondary axis
ax2 = ax.twinx()
ax2.plot(grace_yearly['0'], label='State Average LWE', color='k',zorder=1)
ax2.set_ylim([15, -15])
ax2.set_ylabel(u'Δ LWE (cm)',fontsize=fsize)
ax2.legend(loc='lower right')

plt.savefig(figurepath+Name, bbox_inches = 'tight')

# %%

# %%
