import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

plt.rc('figure', figsize=(11, 9))
plt.rc('font', size=13)

import requests
import os
from datetime import timedelta, datetime as dt

from acquire import get_store_data

############################ Plot Distributions for a Column ##################################

def hist_plot(df, col, unit_label='', bins=10):
    """
    This function takes in a DataFrame, 
    a string for column name or list,
    a string for unit label, default empty,
    and an integer for number of bins, default 10, and
    displays the distribution of the column.
    """
    plt.hist(df[col], bins=bins, color='thistle', ec='black')
    plt.title('Distribution of ' + col)
    plt.xlabel(unit_label)
    plt.ylabel('Count')
    plt.show()

############################# Function for numeric distributions #################################

def numeric_hists(df, bins=20):
    """
    Function to take in a DataFrame, bins default 20,
    select only numeric dtypes, and
    display histograms for each numeric column
    """
    num_df = df.select_dtypes(include=np.number)
    num_df.hist(bins=bins, color='thistle', ec='black')
    plt.suptitle('Numeric Column Distributions')
    plt.show()

######################## Function to acquire df and prep store data ####################

def prepped_store_df():
    """
    Function to acquire and prepare
    store dataframe and show
    distributions for numeric columns
    """
    # Acquire the df
    df = acquire.get_store_data()
    
    # Convert sale_date to DateTimeIndex
    df['sale_date'] = pd.to_datetime(df.sale_date)
    df = df.set_index('sale_date').sort_index()
    
    # Create date part columns
    df['month'] = df.index.month
    df['weekday'] = df.index.day_name()
    
    # Create calculated columns
    df = df.assign(sales_total = df.sale_amount * df.item_price)
    df = df.assign(sales_diff = df.sales_total.diff(periods=1))
    
    # Change dtypes of numeric columns to object and category
    df = (df.astype({'sale_id': object, 'store_id': object, 
                     'store_zipcode': object, 'item_id': object, 
                     'item_upc12': object, 'item_upc14': object, 
                     'month': 'category', 'weekday': 'category'}))
    
    # Display distributions of numeric columns
    numeric_hists(df)