# === DROUGHT INDICE PREPROCESSING ===
# Written by Danielle Tadych, May 2022
#    modified 06/10/2024

# The purpose of this code is to pick out severe drought periods.

# The dataset needed is NOA National Centers for Environmental Information.
# This data in particular is averaged for the state of Arizona.

# Link to download PDSI:
#   https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/2/pdsi/1/0/1895-2024

# Link to download PHDI:
#   https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/2/phdi/1/0/1895-2024
# %% Load the packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Assign Data paths
inputpath = '../../Data/Input'
shapepath = '../../Data/Input/Shapefiles'
outputpath = '../../Data/Output/Local'
# %% Input the date you downloaded these files
date_downloaded = "06102024"

# %% Creating colors
drought_color = '#ffa6b8'
wet_color = '#b8d3f2'

# %% Read in the files
filename = 'NOAA_PDSI_Timeseries.csv'
pdsi = pd.read_csv(f'{inputpath}/'+filename, header=2)
pdsi['Date'] = pd.to_datetime(pdsi['Date'], format='%Y%m', errors='coerce').dropna()
pdsi['In_year'] = pdsi['Date'].dt.year
pdsi

filename = 'NOAA_PHDI_Timeseries.csv'
phdi = pd.read_csv(f'{inputpath}/'+filename, header=2)
phdi['Date'] = pd.to_datetime(phdi['Date'], format='%Y%m', errors='coerce').dropna()
phdi['In_year'] = phdi['Date'].dt.year
phdi

# %% Average from monthly to yearly
yearly_pdsi_new = pd.pivot_table(pdsi, index=["In_year"], values=["Value"], dropna=False, aggfunc=np.mean)
yearly_pdsi_new = yearly_pdsi_new.rename(columns = {'Value':'PDSI'})

yearly_phdi_new = pd.pivot_table(phdi, index=["In_year"], values=["Value"], dropna=False, aggfunc=np.mean)
yearly_phdi_new = yearly_phdi_new.rename(columns = {'Value':'PHDI'})

# %% Assign severe threshold
value = 3
yearly_pdsi_new['wet'] = value
yearly_pdsi_new['dry'] = -value

# %% Create a python database of both PDSI & PHDI together
yearly_new_indices = yearly_pdsi_new.copy()
yearly_new_indices['PHDI'] = yearly_phdi_new['PHDI']
yearly_new_indices

# %% Plot to see what it looks like
# (This is graph is basically Figure 3a)
# Will need to add more shading if you're updating the data
value = 3 # Severe drought cutoff value

ds = yearly_new_indices
minyear=1975
maxyear=2023
name = "Average PDSI and PHDI for AZ from " + str(minyear) + " to " + str(maxyear)
min_y = -6
max_y = 6
fsize = 12

ds['wet'] = value
ds['dry'] = -value

fig, ax = plt.subplots(figsize = (9,5))

ax.plot(ds['PHDI'], label='PHDI'
        # , color='blue'
        , lw=3
        ) 
ax.plot(ds['PDSI']
        # ,'-.'
        , label='PDSI'
        # , color='default'
        , lw=2
        ) 

# Severe Drought Shading
a = 1988
b = 1990
c = 1995
d = 1996
e = 2021
f = 2022
g = 2002
h = 2004
i = 2005
j = 2008
k = 2012
l = 2015
m = 2018
n = 2019
plt.axvspan(a, b, color=drought_color, alpha=0.5, lw=0, label="Severe Drought")
plt.axvspan(c, d, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(e, f, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(g, h, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(i, j, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(k, l, color=drought_color, alpha=0.5, lw=0)
plt.axvspan(m, n, color=drought_color, alpha=0.5, lw=0)

# ax.plot(ds['wet'],label='wet',color='black',zorder = 5)
ax.plot(ds['dry'],'-.',label='Cutoff Value',color='black', zorder=5)

ax.set_xlim(minyear,maxyear)
ax.set_ylim(min_y,max_y)
ax.minorticks_on()
ax.grid(visible=True,which='major')
ax.grid(which='minor',color='#EEEEEE', lw=0.8)
ax.set_title(name, fontsize=14)
ax.set_xlabel('Year', fontsize=fsize)
ax.set_ylabel('Index Values',fontsize=fsize)
ax.legend(loc = [1.04, 0.40], fontsize = fsize)
fig.set_dpi(600.0)
# plt.savefig(outputpath+name+'cutoffval_'+str(value), bbox_inches = 'tight')

# %%
analysis_period = yearly_new_indices[yearly_new_indices.index>=1975]
analysis_period.to_csv(f'{inputpath}/Yearly_DroughtIndices_updated{date_downloaded}.csv')
# %%
