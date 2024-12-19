# Drought Analysis and Creating Figures

Run these files to conduct the drought analysis and create figures from our paper where we explore groundwater and drought at different spatial scales in Arizona.

The concept of our workflow is illustrated in the picture shown below.
![Flowchart showing how Depth to Water readings (DTW) are plotted against time to create a trendline (least squares regression).  The DTW values are then subtracted by the trendline to calculate anomalies.  Anomalies are plotted against time.  Maximum drawdown is the maximum anomaly within a severe drought period.](../../Figures/Figure1.png)

### Requirements:
Must have downloaded files and run codes described in DataPreprocessing before continuing.

### Workflow:
1. StatewideAnalysis.ipynb
    - This notebook conducts an analysis of well and GRACE data at the statewide scale.
    - Creates Figures 3-4.
2. RegionalAnalysis.ipynb
    - This notebook conducts a regional analysis on our filtered well database.
    - Creates Figures 5-6
3. IndividualWells.ipynb
    - This notebook calculates the slopes and maximum drawdown of each individual well used in this analysis.  The data from this notebook was used to create statewide maps.
    - outputs data used for Figure 7, although Figure 7 was created in QGIS.
4. Case Studies
    - This is a series of notebooks used in our case study analysis. <br>
        - a. Casestudy_analysis_AllShapes.ipynb
            - this notebook creates graphs based on a shapefile with multiple polygons.  It was created so we could have more versatility with creating graphs of our case studies.  It is basically a combination of the Regional Analysis workflow and Casestudy workflow (see b). <br>
            - Creates Figures 8-10 except for maps which were created in QGIS
        - b. Casestudy_Analysis.ipynb (optional)
            - this notebook creates graphs based on a shapefile of a single polygon <br>
            - It can be used for preliminary analysis.
        - c. CasestudyAnalysis_FlagstaffSpecial.ipynb (optional)
            - this notebook was created to determine if there was skewing of the data for our Flagstaff polygon.
            - there are only a few wells which match our filtering criteria so we made timeseries of those wells.
            - We then categorized them by drilling depth to create timeseries of shallow, midrange, and deep wells just for that polygon.

You're done!  Go check out your new figures created in the Figures folder.  Compare it to items in "Correct" to see if you got the same output!