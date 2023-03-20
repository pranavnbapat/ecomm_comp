import glob
from os.path import exists, join
import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re
prog = re.compile(r'\d*[.]\d*')
path = "data"
extension = 'csv'
matched_path = 'data/matched'
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

df_columns = ['price', 'source','timestamp', 'link', 'title']


def get_amazon_price(session, link, retry=0):
    if retry == 5:
        return ''
    time.sleep(retry)  # seems to not like being spammed with requests
    response = session.get(link, headers=my_headers)
    if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')

        soup = BeautifulSoup(str(html_soup), features='lxml')

        price = soup.find("span", attrs={"class": "a-offscreen"})
        title = soup.find('meta', attrs={'name': 'title'}).get('content')
        price_dict = soup.find('div', attrs={"class": "a-section aok-hidden simpleBundleJavascriptParameters"})
        # price_dict_text = str(get_child_Tag(price_dict).contents[0])
        # all_items="can be found in price_dict_text but I think I dont need to use it as it doesnt give me more data"
        try:
            text_price = price.text
        except:
            return '', title
        if "€" in text_price:
            return text_price.replace('€', "").replace(',', '.'), title
        else:
            return text_price, title
    else:
        return get_amazon_price(session, link, retry + 1)


def get_bol_price(session, link):
    response = session.get(link, headers=my_headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    # price = soup.find("div", attrs={"class": "price-block__price"})
    possible_data = soup.find('div', attrs={'data-test': "taxonomy_data"}).text
    data = eval(possible_data.strip())
    if data:
        item_data = data['pdpTaxonomyObj']['productInfo'][0]
        price = item_data['price']
        title = item_data['title']
        return price, title
    else:
        return '', ''


def make_empty_df():
    df = pd.DataFrame(columns=df_columns)
    return df


def make_row_of_df(data):
    df = pd.DataFrame(data=data, columns=df_columns)
    return df


def do_rounds():
    for file in files:
        file_products = file.replace(matched_path, products_path).replace('.csv', '')
        if exists(file_products):
            continue
        else:
            os.makedirs(file_products)
            df = pd.read_csv(file)
            for i in range(len(df)):
                frame = make_empty_df()
                frame.to_csv(join(file_products, f"Product_{i}.csv"), index=False)
    for file in files:
        session = requests.Session()
        df = pd.read_csv(file)
        file_products = file.replace(matched_path, products_path).replace('.csv', '')
        for i in range(len(df)):
            df_file_path = join(file_products, f"Product_{i}.csv")

            links = df.iloc[i]
            bol_link = links['Bol link']
            amazon_link = links['Amazon link']
            try:
                bol_price, bol_title = get_bol_price(session, bol_link)
            except:
                bol_price = ''
                bol_title = ''
                session = requests.Session()
            try:
                amazon_price, amazon_title = get_amazon_price(session, amazon_link)
            except:
                amazon_price = ''
                amazon_title = ''
                session = requests.Session()
            if not prog.match(amazon_price):
                amazon_price=''
            if not prog.match(bol_price):
                bol_price=''
            timestamp = str(datetime.now())
            data = [[bol_price,'Bol', timestamp, bol_link, bol_title],[amazon_price,'Amazon',timestamp, amazon_link, amazon_title]]
            new_row = make_row_of_df(data)
            old_df = pd.read_csv(df_file_path)
            new_df = pd.concat([old_df, new_row])
            new_df.to_csv(df_file_path, index=False)


if __name__ == '__main__':
    print("starting rounds")
    do_rounds()
    print('done')