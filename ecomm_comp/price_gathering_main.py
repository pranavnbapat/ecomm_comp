import glob
import pandas as pd
import sys
from os.path import join
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
from pathlib import Path
from nltk.corpus import stopwords

path = "data"
extension = 'csv'
products_path='products'
files = glob.glob(path + "/*." + extension)
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
    """
    price_start = text.find('[')
    price_end = text.find(']')
    if price_end != -1:
        price_dictionary = text[price_start+1:price_end]
        price_dictionary = price_dictionary.replace('true','True')
        price_dict = eval(price_dictionary)
        if isinstance(price_dict,tuple):
            price_dict=price_dict[0]
        return price_dict.get('priceAmount')
    else:
        return ''
        """
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


if __name__ == '__main__':
    data = None
    for file in files:
        if 'main' in file:
            data = pd.read_csv(file)

    if data is None:
        print('no data found')
        sys.exit(2)
    b=2
    session = requests.Session()
    for index,row in data.iterrows():
        links = list(row.array)
        path_to_csv = join(products_path,f"Product_{index}.csv")
        bol = links[0]
        amazon = links[1]
        a_price=get_amazon_price(session,amazon)
        b_price=get_bol_price(session,bol)

        print(f'price {a_price} for {amazon}')
        print(f'price {b_price} for {bol}')