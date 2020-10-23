import requests
import pandas as pd
import os
from env import host, user, password
#################### API Imports ############################

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def read_csv_url_csv(url):
    '''
    This function follows a url to a csv and reads in the csv from the url
    '''
    df = pd.read_csv(url)
    return df

def get_csv_url_data(file_name, url, cached=False):
    '''
    This function reads in data fr if cached == False 
    or if cached == True reads in df from a csv file, returns df
    '''
    if cached or os.path.isfile(file_name) == False:
        df = read_csv_url_csv(url)
    else:
        df = pd.read_csv(file_name, index_col=0)
    return df

