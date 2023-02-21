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
from scraping_general import *
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

def get_amazon_price(session,link,retry=0):
    if retry==5 :
        return''
    time.sleep(retry) # seems to not like being spammed with requests
    response = session.get(link, headers=my_headers)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')

        soup = BeautifulSoup(str(html_soup), features='lxml')

        price = soup.find("span", attrs={"class": "a-offscreen"})
        price_dict = soup.find('div',attrs={"class":"a-section aok-hidden simpleBundleJavascriptParameters"})
        #price_dict_text = str(get_child_Tag(price_dict).contents[0])
       # all_items="can be found in price_dict_text but I think I dont need to use it as it doesnt give me more data"
        try:
            text_price = price.text
        except:
            b=2
        if "€" in text_price:
            return text_price.replace('€',"").replace(',','.')
        else:
            return ''
    else:
        return get_amazon_price(session,link,retry+1)
def get_bol_price(session,link):
    response = session.get(link, headers=my_headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    #price = soup.find("div", attrs={"class": "price-block__price"})
    possible_data = soup.find('div',attrs={'data-test': "taxonomy_data"}).text
    data = eval(possible_data.strip())
    if data:
        item_data = data['pdpTaxonomyObj']['productInfo'][0]
        price = item_data['price']
        title = item_data['title']
        return price
    else:
        return ''
    #
    # try:
    #     text = price.text.replace('-','').strip()
    # except:
    #     b=2
    # if '\n' in text:
    #     double_price = text.split()
    #     return '.'.join(double_price)
    # else:
    #     return text
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
    print('done')
