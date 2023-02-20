import glob
import pandas as pd
import sys
from os.path import exists,join
import collections as cl
import os
import requests
import time
import re
import pandas as pd
import nltk
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
path = "data"
extension = 'csv'
matched_path='data/matched'
files = glob.glob(matched_path + "/*." + extension)
my_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Accept": "text/html,application/json,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Cache-Control": "no-cache",
    'Connection': 'keep-alive',
    'Origin': 'https',
    'Pragma': 'no-cache',
    'Referer': 'https',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin'
}
products_path = 'products'

df_columns=['bol_price','amazon_price','timestamp']

def get_amazon_price(session,link):
    response = session.get(link, headers=my_headers)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    soup = BeautifulSoup(str(html_soup), features='lxml')

    price = soup.find("span", attrs={"class": "a-offscreen"})
    text_price = price.text
    if "€" in text_price:
        return text_price.replace('€',"").replace(',','.')
    else:
        return ''
def get_bol_price(session,link):
    response = session.get(link, headers=my_headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    price = soup.find("div", attrs={"class": "price-block__price"})
    text = price.text.replace('-','').strip()
    if '\n' in text:
        double_price = text.split()
        return '.'.join(double_price)
    else:
        return text
def make_empty_df():
    df = pd.DataFrame(columns=df_columns)
    return df
def make_row_of_df(data):
    df = pd.DataFrame(data=data,columns=df_columns)
    return df
def do_rounds():
    for file in files:
        file_products = file.replace(matched_path,products_path).replace('.csv','')
        print(file_products)
        if exists(file_products):
            continue
        else:
            os.makedirs(file_products)
            df = pd.read_csv(file)
            for i in range(len(df)):
                frame = make_empty_df()
                frame.to_csv(join(file_products,f"Product_{i}.csv"),index=False)
    for file in files:
        session = requests.Session()
        df = pd.read_csv(file)
        file_products = file.replace(matched_path, products_path).replace('.csv', '')
        for i in range(len(df)):
            df_file_path = join(file_products,f"Product_{i}.csv")

            links = df.iloc[i]
            bol_link = links['Bol link']
            amazon_link = links['Amazon link']

            bol_price=get_bol_price(session,bol_link)
            amazon_price=get_amazon_price(session,amazon_link)
            timestap=str(datetime.now())

            data = [[bol_price,amazon_price,timestap]]

            new_row = make_row_of_df(data)
            old_df = pd.read_csv(df_file_path)
            new_df = pd.concat([old_df,new_row])
            new_df.to_csv(df_file_path,index=False)

if __name__ == '__main__':
    do_rounds()

