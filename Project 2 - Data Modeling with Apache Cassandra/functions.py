import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv

def preprocessing_csv_files(pwd):
    """
    - Merges all the csv files from event_data folder.
    
    - Selects only certain columns.
    
    - Creates a new csv file with the combined data.
    """
    
    # 1. Create list of filepaths to process original event csv data files

    # get the current folder and subfolder event data
    filepath = os.getcwd() + '/event_data'

    # create a list of files and collect each filepath
    for root, dirs, files in os.walk(filepath):
    
    # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root,'*'))


    # 2. Process the files to create the combined csv data file

    # initiate an empty list of rows that will be generated from each file
    full_data_rows_list = [] 

    # for every filepath in the file path list:
    for f in file_path_list:

    # a. read csv file
        with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            next(csvreader)

     # b. extract each data row one by one and append it        
            for line in csvreader:
                full_data_rows_list.append(line) 

    #print(full_data_rows_list)
    
    # select only certain columns and place the data into the combined file event_datafile_new.csv
    # this file will be used to fill our database tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',\
                    'level','location','sessionId','song','userId'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))