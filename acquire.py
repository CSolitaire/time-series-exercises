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

################################################################################################################

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

def get_store_data():
    """
    This function checks for csv files
    for items, sales, stores, and big_df 
    if there are none, it creates them.
    It returns one big_df of merged dfs.
    """
    # check for csv files or create them
    if os.path.isfile('items.csv'):
        items_df = pd.read_csv('items.csv', index_col=0)
    else:
        items_df = get_df('items')
        
    if os.path.isfile('stores.csv'):
        stores_df = pd.read_csv('stores.csv', index_col=0)
    else:
        stores_df = get_df('stores')
        
    if os.path.isfile('sales.csv'):
        sales_df = pd.read_csv('sales.csv', index_col=0)
    else:
        sales_df = get_df('sales')
        
    if os.path.isfile('big_df.csv'):
        df = pd.read_csv('big_df.csv', index_col=0)
        return df
    else:
        # merge all of the DataFrames into one
        df = pd.merge(sales_df, stores_df, left_on='store', right_on='store_id').drop(columns={'store'})
        df = pd.merge(df, items_df, left_on='item', right_on='item_id').drop(columns={'item'})

        # write merged DateTime df with all data to directory for future use
        df.to_csv('big_df.csv')
        return df

################################################################################################################

def opsd_germany_daily():
    """
    This function uses or creates the 
    opsd_germany_daily csv and returns a df.
    """
    if os.path.isfile('opsd_germany_daily.csv'):
        df = pd.read_csv('opsd_germany_daily.csv', index_col=0)
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url)
        df.to_csv('opsd_germany_daily.csv')
    return df


