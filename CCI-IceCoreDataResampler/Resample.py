'''
Author: Heather M. Clifford

Resample Software for Ice Core Data

Date Created: 5/14/2018
Date Modified: 5/14/2018

--------------------------------------------------------------------------------
This software is designed to resample data based on either Year or Depth or both
    by increments specified by the user. The user input consists of filename,
    which of Year or Depth to resample by, and the amounts to resample by.

    USER INPUT:
        Resample.py Filename By Increments*

        Filename: user specified name of file to resample
            - this file should be placed in the data directory

        By: user specified name to resample data by, options include:
            DEPTH: 'depth','Depth','DEPTH'
            YEAR: 'year','Year','age','Age','Time','YEAR','AGE'
            ALL: 'All', 'ALL', 'Both','BOTH'
                 (will resample by both depth and age for given increment amounts)
            - used to find columns that start or end with the respective strings

        Increments: user specified increment amounts to resample the data by
            - User may input multiple numbers

    OUTPUT:
        CSV and PDF files corresponding to the user input
--------------------------------------------------------------------------------
'''

import pandas as pd
import os
import numpy as np
import sys
from scripts.func import frange
from math import isnan
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from typing import List, Tuple

def file_to_dataframe(file:str) -> pd.DataFrame:
    '''
    ------------------------------------------------------------
    file_to_dataframe functions

    - used to input file from user input
    ------------------------------------------------------------
    Input:
        file : string from user input of file

    Output:
        data : pd.DataFrame from user input file
    ------------------------------------------------------------
    '''
    if file.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.endswith('.xlsx'):
        data = pd.read_excel(file)
    elif file.endswith('.txt'):
        data = pd.read_table(file)
    else:
        print('Dataset inputted is not an .csv, .xlsx or .txt, change file type')

    return data

def find_by_columns(data:pd.DataFrame,by:str) -> Tuple[List,str]:
    '''
    ------------------------------------------------------------
    find_by_columns function

    - used to determine which columns to resample by in Dataset
    ------------------------------------------------------------
    Input:
        data : pd.DataFrame of user input Dataset
        by   : user input string to resample by (year or depth or all)

    Output:
        by   : list of column names to resample by
        name : generic name of either Depth or Year
    ------------------------------------------------------------
    '''
    if (by.startswith(('Depth','depth'))):
        by =  [i for i in data.columns if (i.startswith(('depth','Depth','DEPTH'))) \
                | (i.endswith(('depth','Depth','DEPTH')))]
        name = 'Depth'
    elif (by.startswith(('year','Year','age','Age','Time','YEAR','AGE'))):
        by =  [i for i in data.columns if (i.startswith(('year','Year','age','Age','Time','YEAR','AGE'))) \
                | (i.endswith(('year','Year','age','Age','Time','YEAR','AGE')))]
        name = 'Year'
    elif (by.startswith(('all','All','ALL','Both','BOTH'))):
        by1 =  [i for i in data.columns if (i.startswith(('depth','Depth','DEPTH'))) \
                | (i.endswith(('depth','Depth','DEPTH')))]
        by2 =  [i for i in data.columns if (i.startswith(('year','Year','age','Age','Time','YEAR','AGE'))) \
                | (i.endswith(('year','Year','age','Age','Time','YEAR','AGE')))]
        by = [by1,by2]
        name =['Depth','Year']

    else:
        print('by is not found as year or depth, input by as year or depth')

    return by,name

def check_resample(n_idx:List,inc_amt:float) -> float:
    '''
    ------------------------------------------------------------
    check_resample function

    - used to find discrepency due to decreasing resolution, will find end
        point of Dataset where there are more than 5 indexes with all NaN
        values in a row
    ------------------------------------------------------------
    Input:
        n_idx      : list of index where all NaNs values are found
                        ( Area of dataset where not enough points to get mean)
        inc_amt    : increment amount to resample data by

    Output:
        stop_point : index values when there are more than 5 indexes
                        with all NaN values in a row
    ------------------------------------------------------------
    '''
    z = 0
    n_idx.reverse()

    for i in range(1,len(n_idx)-1):
        if n_idx[i]+inc_amt ==n_idx[i-1]:
            z=z+1
            if z == 5:
                stop_point = n_idx[i]
                print("Due to decreasing resolution of the data, we are not able to resample below the end point")
                print('end point = {}'.format(stop_point))
                return stop_point

def set_index(df:pd.DataFrame,by:str) -> pd.DataFrame:
    '''
    ------------------------------------------------------------
    set_index function

    - used to set index of dataframe by given column name
    ------------------------------------------------------------
    Input:
        df:      raw Dataset
        by:      column to set as index

    Output:
        df: raw dataset with by as index
    ------------------------------------------------------------
    '''

    if not df.index.name == by:
        try:
            df = df.set_index(by)
        except:
            print('{} is not found as a column in the dataset, insert name of column to resample data by'.format(by))
    return df

def resample(df:pd.DataFrame,by:str,inc_amt:float) -> pd.DataFrame:
    '''
    ------------------------------------------------------------
    resample function

    - used to resample data by increment amounts from min to max of
        given column
    ------------------------------------------------------------
    Input:
        df:      pd.DataFrame
        inc_amt: Increment Amount
        by:      Column to resample data by

    Output:
        df: pd.DataFrame resampled by user input column
    ------------------------------------------------------------
    '''
    top = int(df.index.min())
    bot = int(df.index.max())
    inc = inc_amt/2

    range_list = list(frange(top,bot,inc_amt))

    df_new = pd.DataFrame()

    n_idx =[]
    for i in range_list:
        idx = df[( df.index >=i-inc) & ( df.index < i+inc)]
        df_new = df_new.append(idx.mean(),ignore_index=True)

        if idx.mean().isnull().all():
            n_idx.append(i)

    end = check_resample(n_idx,inc_amt)


    df_new = df_new.set_index(pd.Series(range_list))
    df_new.index.name = by
    df_new = df_new[::-1]
    df_new = df_new.loc[:end]

    return df_new

def create_output_filename_and_folders(by:str,inc_amt:float,name:str) -> str:
    '''
    ------------------------------------------------------------
    output function

    - used to create folder and csv files for resampled output of data
    ------------------------------------------------------------
    Input:
        by      : column name to resample data by
        inc_amt : increment amount
        name    : name of objective to resample by (Year or Depth)


    Output:
        outfile : output file name and path
    ------------------------------------------------------------
    '''
    folder = os.path.join(os.getcwd(), 'output_files')
    if not os.path.exists(folder):
        os.makedirs(folder)

    filefolder = os.path.join(folder, base)
    if not os.path.exists(filefolder):
        os.makedirs(filefolder)

    namefolder = os.path.join(filefolder,"Resampled_by_{}".format(name))
    if not os.path.exists(namefolder):
        os.makedirs(namefolder)

    incfolder = os.path.join(namefolder,"{}".format(inc_amt))
    if not os.path.exists(incfolder):
        os.makedirs(incfolder)

    filename = '{}_{}_r{}'.format(base,by.replace(" ", "_"),inc_amt)
    outfile =os.path.join(incfolder,filename)
    return outfile

def output(data:pd.DataFrame,raw_data:pd.DataFrame,outfile:str):
    '''
    ------------------------------------------------------------
    output function

    - used to create folder and csv files for resampled output of data
    ------------------------------------------------------------
    Input:
        data     : resampled dataset
        raw data : raw dataset
        outfile  : output file and path for data


    Output:
        csv and pdf files of resampled data
    ------------------------------------------------------------
    '''
    outfile_base = os.path.basename(outfile)
    print("")
    print("Creating output csv file : {}".format(outfile_base))

    data.to_csv(outfile+'.csv')

    print("Creating output pdf plot file : {}".format(outfile_base))

    plot_output(data,raw_data,outfile+'_log.pdf',True)
    plot_output(data,raw_data,outfile+'.pdf',False)

def plot_output(data:pd.DataFrame,raw_data:pd.DataFrame,outfile:str,log):
    '''
    ------------------------------------------------------------
    plot_output function

    - used to create plots of all samples in dataset in normal and log scale
    ------------------------------------------------------------
    Input:
        data     : resampled dataset
        raw data : raw dataset
        outfile  : output file and path for data
        logy     : boolean for log or normal scale (True - log, False - normal)


    Output:
        pdf files of resampled and raw data in normal and log scale
    ------------------------------------------------------------
    '''
    with PdfPages(outfile) as pdf:
        for i in data.columns:
            ax = raw_data[i].plot(figsize=(8,5), color = 'gray',legend=True)
            data[i].plot(ax=ax,color = 'firebrick')
            if log:
                ax.semilogy()
            ax.legend(['{}: Resampled'.format(i),'{}: Raw'.format(i)])
            plt.tight_layout()
            fig = plt.gcf()
            pdf.savefig(fig)
            plt.close()

def set_resample(raw_data_input:pd.DataFrame,by:str,inc_amt:float,name:str):
    '''
    ------------------------------------------------------------
    set_resample function

    - used to run through sets of user specified inputs to resample
    ------------------------------------------------------------
    Input:
        raw_data_input : raw data in a DataFrame from user input
        by             : columns to resample data by
        inc_amt        : increment amount

    Output:
        PDF and CSV files
    ------------------------------------------------------------
    '''
    for b in by:
        print("")
        print('Resampling by {} : {} '.format(name,b))
        for i in inc_amt:
            print("")
            print("Resampling for {} Increment Amount: {}".format(name, i))
            raw_data = set_index(raw_data_input,b)
            resampled = resample(raw_data,b,i)
            outfile = create_output_filename_and_folders(b,i,name)
            output(resampled,raw_data,outfile)

def user_input(raw_data_input:pd.DataFrame,by:str,inc_amt:float,name:str):
    '''
    ------------------------------------------------------------
    user_input function

    - used to determine the sets of data to resample
    ------------------------------------------------------------
    Input:
        raw_data_input : raw data in a DataFrame from user input
        by             : columns to resample data by
        inc_amt        : increment amount

    Output:
        PDF and CSV files
    ------------------------------------------------------------
    '''

    if type(name)==list:
        print("")
        print('Resample by Year & Depth')
        for n in range(len(name)):
            set_resample(raw_data_input,by[n],inc_amt,name[n])
    else:
        print("")
        print('Resample by {}'.format(name))
        set_resample(raw_data_input,by,inc_amt,name)

file = sys.argv[1]
base = os.path.basename(file)[:-4]
raw_data_input = file_to_dataframe(os.path.join('data',file))
by,name = find_by_columns(raw_data_input,sys.argv[2])
inc_amt = [float(i) for i in sys.argv[3:]]

user_input(raw_data_input,by,inc_amt,name)
