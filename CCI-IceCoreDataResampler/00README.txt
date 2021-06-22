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

	~~~Example: Resample.py Icecoredata.csv Years 5 10 20

        Filename: user specified name of file to resample
	    - this file should be .csv, .xlsx or .txt
            - this file should be placed in the data directory

        By: user specified name to resample data by, options include:
            DEPTH: 'depth','Depth','DEPTH'
            YEAR: 'year','Year','age','Age','Time','YEAR','AGE'
            ALL: 'All', 'ALL', 'Both','BOTH'
            	 (will resample by both depth and age for given increment amounts)
            - used to find columns that start or end with the respective strings

        Increments: user specified increment amounts to resample the data by
            - *User may input multiple numbers

    OUTPUT:
        CSV & PDF files corresponding to the user input
--------------------------------------------------------------------------------
