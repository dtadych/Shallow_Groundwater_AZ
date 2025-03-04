# Data Preprocessing

Run items in this folder to move on to the stream analysis (FigureCreation).

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
2. Download NHD+ High Res
3. Download Stream Gauge Data
     - Since it can take a while for usgs to consolidate and we first wanted recent data, this data was originally downloaded in batches based on time periods
        1) 2000-2025 with filename "USGS_Streamgauges"
        2) 1980-1999 with filename "USGS_Streamgauges_19801999"
     - Save it as a tab delimmited file in the Data/Input folder.  This can sometimes take a while to run and download

 ### Run Codes
 1. First, need to merge the well databases.  Make sure all filepaths match where the new data has landed.
    - Run 1a_WellStaticMerge.py
      - This code creates databases that contain all static information about the wells from ADWR
    - Run 1b_WellTSMerge.py
      - This code pulls water level data from both databases to create timeseries of all wells (even if some wells just have one reading)