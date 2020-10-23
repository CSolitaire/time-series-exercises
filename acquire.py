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

def api_request():
    '''
    This function retrieves all items of all pages
    from the base url api and saves it as a dataframe
    '''
    #saving the base url
    base_url = 'https://python.zach.lol'
    #opening/visiting the url
    response = requests.get('https://python.zach.lol/api/v1/sales')
    #saving the data as a json script
    data = response.json()
    #saving the json script as a dataframe
    df = pd.DataFrame(data['payload']['sales'])
    #creating a loop to scan all the items pages
    for number in range(1, data['payload']['max_page']):
        #moving into the next page of items
        response = requests.get(base_url + data['payload']['next_page'])
        #saving the as a json script
        data = response.json()
        #adding the next page of items onto the original dataframe
        df = pd.concat([df, pd.DataFrame(data['payload']['sales'])], ignore_index=True)
    return df