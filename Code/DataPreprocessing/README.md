# Data Preprocessing

Run items in this folder to move on to the drought analysis (FigureCreation).

### Requirements:
 1. Download ADWR's groundwater databases.
     - <a href = 'https://gisdata2016-11-18t150447874z-azwater.opendata.arcgis.com/datasets/34c92af536ec4047aeaf9d93053dc317_0/explore?location=0.015556%2C-111.970052%2C0.00' target='_blank'>Well Registry </a>: catalog of all well permits in Arizona
       - First, save it as csv in Data/Input as "Well_Registry_[mmddyyyy].csv
       - Next, save it as a shapefile in Data/Input/Shapefiles folder
       - Make sure to unzip all files
     - Groundwater Site Inventory (GWSI)</a>: long-term water level measurements
       - First, save the <a href= 'https://www.azwater.gov/sites/default/files/zip/GWSI_ZIP_20240401.zip' target='_blank'>excel form of the database here</a> from the main website into Data/Input
        <br>  - *Note* - This code uses the excel form of this database found on a different webpage than the gis files.
       - Next, save it as a shapefile from the <a href='https://gisdata2016-11-18t150447874z-azwater.opendata.arcgis.com/datasets/azwater::gwsi-app/explore?layer=3&location=34.064362%2C-111.834805%2C6.67' target='_blank'>ADWR GIS Data repository here</a> into Data/Input/Shapefiles folder
       - Make sure to unzip all files
2. Download the latest <a href='https://www2.csr.utexas.edu/grace/RL0602_mascons.html' target='_blank'>GRACE data</a>.
   - Move these files into the Data/Input/Shapefiles folder.
3. Download "georeg_reproject_fixed" files from our <a href='https://datacommons.cyverse.org/browse/iplant/home/shared/commons_repo/curated/Tadych_AzGroundwaterSpatialAnalysis_Aug2023/Data/Shapefiles' target='_blank'>Cyverse database </a>
   - Place in Data/Input/Shapefiles folder.
 
 4. Download Drought indices
     - The dataset needed is from NOAA National Centers for Environmental Information averaged for the state of Arizona.
     - <a href='https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/2/pdsi/1/0/1895-2024' target='_blank'> Link to download PDSI</a>, save it as "NOAA_PDSI_Timeseries.csv" in Data/Input folder
     - <a href='https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/2/phdi/1/0/1895-2024' target='_blank'>Link to download PHDI </a>, save it as "NOAA_PHDI_Timeseries.csv" in Data/Input folder

 ### Run Codes
 1. First, need to merge the well databases.  Make sure all filepaths match where the new data has landed.
    - Run 1a_WellStaticMerge.py
      - This code creates databases that contain all static information about the wells from ADWR
    - Run 1b_WellTSMerge.py
      - This code pulls water level data from both databases to create timeseries of all wells (even if some wells just have one reading)
 2. Second, run spatial analysis scripts
    - Run 2a_SpatialAnalysisGrace.py
      - This script creates a state average of total water storage
    - Run 2b_SpatialAnalysisWells.py
      - This script filters our well database to export wells with at least 15 years of data or more (used for graphing later)
      - Creates water level values by groundwater regulation and by access to surface water
 3. Third, run 3_DroughtIndices.py
    - This script will create yearly averages of pdsi and phdi into a nice and cozy dataset