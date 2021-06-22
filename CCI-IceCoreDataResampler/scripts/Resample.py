'''
Author: Heather Clifford

Resample Function for Ice Core Data


'''

import pandas as pd
import os
import sys


def user_input(file:str):
    if file.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.endswith('.xlsx'):
        data = pd.read_excel(file)
    elif file.endswith('.txt'):
        data = pd.read_table(file)
    else:
        print('Dataset inputted is not an .csv, .xlsx or .txt, change file type')

    return data


def resample(df,inc_amt,by):
    '''
    Resample Function
        Resamples data to increment amounts from min to max of
        given column

    Input:
        df:      DataFrame
        inc_amt: Increment Amount
        by:      Column to resample data by

    Output:
        df: DataFrame resampled by user input column

    '''
    if not type(by) == str:
        by = str(by)

    try:
        df = df.set_index(by)
    except:
        print('{} is not found as a column in the dataset, insert name of column to resample data by'.format(by))

    top = int(df.index.min())
    bot = int(df.index.max())
    inc = inc_amt/2

    range_list = list(range(top,bot,inc_amt))

    df_new = pd.DataFrame()

    for i in range_list:

        idx = df[( df.index >=i-inc) & ( df.index < i+inc)]
        df_new = df_new.append(idx.mean(),ignore_index=True)


    df_new = df_new.set_index(pd.Series(range_list))

    return df_new



# folder = sys.argv[1]

file = sys.argv[1]
inc_amt = sys.argv[2]
by = sys.argv[3]

data = user_input(os.path.join(os.getcwd(),file))
data = resample(data,inc_amt,by)
