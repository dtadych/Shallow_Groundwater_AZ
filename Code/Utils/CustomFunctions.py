import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr, pearsonr

figurepath = '../../Figures/Local/'

# Function to calculate slope using linear regression
def calculate_slope(y):
    x = np.arange(len(y))
    slope, _ = np.polyfit(x, y, 1)
    return slope

# Functions for correlations
def kendall_pval(x,y):
        return kendalltau(x,y)[1]
    
def pearsonr_pval(x,y):
        return pearsonr(x,y)[1]
    
def spearmanr_pval(x,y):
        return spearmanr(x,y)[1]

def correlation_test(water_dataset, drought_dataset, drought_indice, lag,test_dataset_name,colors_list,label_list,vert_axis_label):
    """ This function is testing to see if there is a correlation between two datasets, 
    more specificially, a water dataset and a drought dataset.

    Water_dataset: Can be any water dataset
    drought_dataset: the drought dataset created 
    drought_indice: The drought indice (in our case, PDSI or PHDI) as a string
    lag: If doing shifted correlation test
    test_dataset_name: Name of the test you're running in string form.
    colors_list: A list of colors
    label_list: A list of better label strings that match the datasets
    vert_axis_label#: What to call the vertical axis
    
    Example code: 
    test_name = "ADWR Well Anomalies ("+str(minyear_wells)+"-"+str(maxyear)+")"
    ds = dtw_anomalys_AZwells
    drought = drought_indices_wells
    lag = 0        # If running a shifted correlation analysis,
                  change this to however many # years; 0 is no lag
    indice = 'PDSI'
    result = cf.correlation_test(ds, drought, indice, lag,test_name)
    print(result)
    """
    output = ""
    columns = water_dataset.columns
    column_list = water_dataset.columns.tolist()
    
    output += "Results for "+test_dataset_name+":\n"
    output += 'Kendall Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  tau = ' + str(round(df1.corr(df2, method='kendall'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=kendall_pval), 4)) + '\n'
    
    output += 'Spearman Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  rho = ' + str(round(df1.corr(df2, method='spearman'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=spearmanr_pval), 4)) + '\n'
    
    output += 'Pearson Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        r = df1.corr(df2, method='pearson')
        output += '  rsq = ' + str(round(r * r, 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=pearsonr_pval), 4)) + '\n'
    
    fig, ax = plt.subplots(figsize = (7,5))
    x = drought_dataset[drought_indice]
    for i,j,k in zip(column_list
                    # ,reg_colors
                    # , SW_colors
                    , colors_list
                    , label_list
                    ):
            y = water_dataset[i]
            ax.scatter(x,y
                    , label=k
                    , color=j
                    )
            # Trendline: 1=Linear, 2=polynomial
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x),'-'
                    , color=j
                    # ,label=(k+' Trendline')
                    )


    ax.set_xlabel(drought_indice)
    ax.set_ylabel(vert_axis_label)
    ax.set_title("Comparing "+drought_indice+" with "+test_dataset_name,loc='center',fontsize=14,pad=15)
    # ax.set_ylim(0,400)
    fig.set_dpi(600)
    plt.legend(loc = [1.05, 0.40])

    return output

def correlation_test_2y(water_dataset1, water_dataset2, drought_dataset, drought_indice, lag,
                        test_dataset_name1, test_dataset_name2,y1label,y2label,color1,color2,
                        vertical_axis_label1,vertical_axis_label2,subplot_title):
    """ This function is testing to see if there is a correlation between three datasets, 
    more specificially, 2 water datasets against a drought dataset.

    Water_dataset#: Can be any water dataset
    drought_dataset: the drought dataset created 
    drought_indice: The drought indice (in our case, PDSI or PHDI) as a string
    lag: If doing shifted correlation test
    test_dataset_name#: Name of the test you're running in string form.
    y#label: whatever you want on the legend for your dataset as a string
    color#: any color
    vert_axis_label#: What to call the vertical axis

    Example code: 
    ds = lwe_anomalys_grace
    ds2 = dtw_anomalys_AZwells
    drought = drought_indices_wells

    indice = 'PDSI'
    # If running a shifted correlation analysis,
    #    change this to however many # years; 0 is no lag
    lag = 0

    betterlabels = 'GRACE' 
    betterlabels2 = 'AZ Wells' 

    test_name = "GRACE Anomaly Correlation"
    test_name2 = "ADWR Well Anomalies"

    sublot = 'b)'

    result = cf.correlation_test_2y(ds,ds2,drought,indice,lag
                                ,test_name,test_name2
                                ,betterlabels,betterlabels2
                                ,grace_color,az_wells_color)
    print(result)
    """
    output = ""
    columns = water_dataset1.columns
    column_list = water_dataset1.columns.tolist()
    columns2 = water_dataset2.columns
    column_list2 = water_dataset2.columns.tolist()
    betterlabels = [y1label] 
    betterlabels2 = [y2label] 
    
    output += "Results for "+test_dataset_name1+":\n"
    output += 'Kendall Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset1[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  tau = ' + str(round(df1.corr(df2, method='kendall'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=kendall_pval), 4)) + '\n'
    
    output += 'Spearman Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset1[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  rho = ' + str(round(df1.corr(df2, method='spearman'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=spearmanr_pval), 4)) + '\n'
    
    output += 'Pearson Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset1[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        r = df1.corr(df2, method='pearson')
        output += '  rsq = ' + str(round(r * r, 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=pearsonr_pval), 4)) + '\n'
    
    output += "\n"
    output += "Results for "+test_dataset_name2+":\n"
    output += 'Kendall Correlation coefficient\n'
    for i in column_list2:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset2[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  tau = ' + str(round(df1.corr(df2, method='kendall'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=kendall_pval), 4)) + '\n'
    
    output += 'Spearman Correlation coefficient\n'
    for i in column_list2:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset2[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  rho = ' + str(round(df1.corr(df2, method='spearman'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=spearmanr_pval), 4)) + '\n'
    
    output += 'Pearson Correlation coefficient\n'
    for i in column_list2:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset2[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        r = df1.corr(df2, method='pearson')
        output += '  rsq = ' + str(round(r * r, 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=pearsonr_pval), 4)) + '\n'
    
    # Scatterplot of correlation values
    fig, ax = plt.subplots(figsize=(7, 5))

    x = drought_dataset[drought_indice]
    x2 = drought_dataset[drought_indice]

    # AZ Wells
    for i, j in zip(column_list2, betterlabels2):
        y2 = water_dataset2[i]
        ax.scatter(x2, y2, label=j, color=color2, marker='x')  # Using marker='x' for differentiation
        z = np.polyfit(x2, y2, 1)
        p = np.poly1d(z)
        ax.plot(x2, p(x2), '-', color=color2)  # Using '--' for differentiation

    # Create a secondary y-axis
    ax2 = ax.twinx()

    # GRACE
    for i, j in zip(column_list, betterlabels):
        y = water_dataset1[i]
        ax2.scatter(x, y, label=j, color=color1)
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), '-', color=color1)

    # Reverse the order of the secondary y-axis
    ax.set_ylim(ax.get_ylim()[::-1])

    # Get the right fontsize for the y-axis
    ax.tick_params(axis='y', labelsize=14)
    ax2.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14, rotation=0)

    ax.set_xlabel(drought_indice, fontsize = 14)
    ax2.set_ylabel(vertical_axis_label1, fontsize = 14)
    ax.set_ylabel(vertical_axis_label2, fontsize = 14)  # Set label for the secondary axis
    ax.set_title('Comparing ' + drought_indice + ' with DTW and GRACE Anomalies\n \n'+subplot_title, loc='left', fontsize = 14,pad=15)
    fig.set_dpi(600)

    # Combine legends for both axes
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='lower right', fontsize = 14)

    plt.show()
    return output

def correlation_test_2y_savefig(water_dataset1, water_dataset2, drought_dataset, drought_indice, lag,
                        test_dataset_name1, test_dataset_name2,y1label,y2label,color1,color2,
                        vertical_axis_label1,vertical_axis_label2,figure_number, subplot_title):
    """ This function is testing to see if there is a correlation between three datasets, 
    more specificially, 2 water datasets against a drought dataset.  

    It has the added functionality to save the figure

    Water_dataset#: Can be any water dataset
    drought_dataset: the drought dataset created 
    drought_indice: The drought indice (in our case, PDSI or PHDI) as a string
    lag: If doing shifted correlation test
    test_dataset_name#: Name of the test you're running in string form.
    y#label: whatever you want on the legend for your dataset as a string
    color#: any color
    vert_axis_label#: What to call the vertical axis
    figure_number: used for saving the file.  Input the number as a string
    subplot_title: used for adding a subplot title and saving the figure.  Put this as a string

    Example code: 
    ds = lwe_anomalys_grace
    ds2 = dtw_anomalys_AZwells
    drought = drought_indices_wells

    indice = 'PDSI'
    # If running a shifted correlation analysis,
    #    change this to however many # years; 0 is no lag
    lag = 0

    betterlabels = 'GRACE' 
    betterlabels2 = 'AZ Wells' 

    test_name = "GRACE Anomaly Correlation"
    test_name2 = "ADWR Well Anomalies"

    sublot = 'b)'

    result = cf.correlation_test_2y(ds,ds2,drought,indice,lag
                                ,test_name,test_name2
                                ,betterlabels,betterlabels2
                                ,grace_color,az_wells_color)
    print(result)
    """
    output = ""
    columns = water_dataset1.columns
    column_list = water_dataset1.columns.tolist()
    columns2 = water_dataset2.columns
    column_list2 = water_dataset2.columns.tolist()
    betterlabels = [y1label] 
    betterlabels2 = [y2label] 
    
    output += "Results for "+test_dataset_name1+":\n"
    output += 'Kendall Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset1[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  tau = ' + str(round(df1.corr(df2, method='kendall'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=kendall_pval), 4)) + '\n'
    
    output += 'Spearman Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset1[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  rho = ' + str(round(df1.corr(df2, method='spearman'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=spearmanr_pval), 4)) + '\n'
    
    output += 'Pearson Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset1[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        r = df1.corr(df2, method='pearson')
        output += '  rsq = ' + str(round(r * r, 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=pearsonr_pval), 4)) + '\n'
    
    output += "\n"
    output += "Results for "+test_dataset_name2+":\n"
    output += 'Kendall Correlation coefficient\n'
    for i in column_list2:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset2[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  tau = ' + str(round(df1.corr(df2, method='kendall'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=kendall_pval), 4)) + '\n'
    
    output += 'Spearman Correlation coefficient\n'
    for i in column_list2:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset2[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  rho = ' + str(round(df1.corr(df2, method='spearman'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=spearmanr_pval), 4)) + '\n'
    
    output += 'Pearson Correlation coefficient\n'
    for i in column_list2:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset2[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        r = df1.corr(df2, method='pearson')
        output += '  rsq = ' + str(round(r * r, 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=pearsonr_pval), 4)) + '\n'
    
    # Scatterplot of correlation values
    fig, ax = plt.subplots(figsize=(7, 5))

    x = drought_dataset[drought_indice]
    x2 = drought_dataset[drought_indice]

    # AZ Wells
    for i, j in zip(column_list2, betterlabels2):
        y2 = water_dataset2[i]
        ax.scatter(x2, y2, label=j, color=color2, marker='x')  # Using marker='x' for differentiation
        z = np.polyfit(x2, y2, 1)
        p = np.poly1d(z)
        ax.plot(x2, p(x2), '-', color=color2)  # Using '--' for differentiation

    # Create a secondary y-axis
    ax2 = ax.twinx()

    # GRACE
    for i, j in zip(column_list, betterlabels):
        y = water_dataset1[i]
        ax2.scatter(x, y, label=j, color=color1)
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), '-', color=color1)

    # Reverse the order of the secondary y-axis
    ax.set_ylim(ax.get_ylim()[::-1])

    # Get the right fontsize for the y-axis
    ax.tick_params(axis='y', labelsize=14)
    ax2.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=14, rotation=0)

    ax.set_xlabel(drought_indice, fontsize = 14)
    ax2.set_ylabel(vertical_axis_label1, fontsize = 14)
    ax.set_ylabel(vertical_axis_label2, fontsize = 14)  # Set label for the secondary axis
    ax.set_title('Comparing ' + drought_indice + ' with DTW and GRACE Anomalies\n \n'+subplot_title, loc='left', fontsize = 14,pad=15)
    fig.set_dpi(600)

    # Combine legends for both axes
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='lower right', fontsize = 14)

    # Save the captured figure
    fig.savefig(figurepath + '/Figure' +figure_number+subplot_title, bbox_inches='tight')

    plt.show()
    return output

def correlation_test_nograph(water_dataset, drought_dataset, drought_indice, lag,test_dataset_name):
    """ This function is testing to see if there is a correlation between two datasets, 
    more specificially, a water dataset and a drought dataset.

    Water_dataset: Can be any water dataset
    drought_dataset: the drought dataset created 
    drought_indice: The drought indice (in our case, PDSI or PHDI) as a string
    lag: If doing shifted correlation test
    test_dataset_name: Name of the test you're running in string form.
    
    Example code: 
    test_name = "ADWR Well Anomalies ("+str(minyear_wells)+"-"+str(maxyear)+")"
    ds = dtw_anomalys_AZwells
    drought = drought_indices_wells
    lag = 0        # If running a shifted correlation analysis,
                  change this to however many # years; 0 is no lag
    indice = 'PDSI'
    result = cf.correlation_test(ds, drought, indice, lag,test_name)
    print(result)
    """
    output = ""
    columns = water_dataset.columns
    column_list = water_dataset.columns.tolist()
    
    output += "Results for "+test_dataset_name+":\n"
    output += 'Kendall Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  tau = ' + str(round(df1.corr(df2, method='kendall'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=kendall_pval), 4)) + '\n'
    
    output += 'Spearman Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        output += '  rho = ' + str(round(df1.corr(df2, method='spearman'), 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=spearmanr_pval), 4)) + '\n'
    
    output += 'Pearson Correlation coefficient\n'
    for i in column_list:
        output += ' ' + str(i) + ':\n'
        df1 = water_dataset[i]
        df2 = drought_dataset[drought_indice].shift(lag)
        r = df1.corr(df2, method='pearson')
        output += '  rsq = ' + str(round(r * r, 3)) + '\n'
        output += '  pval = ' + str(round(df1.corr(df2, method=pearsonr_pval), 4)) + '\n'

    return output
