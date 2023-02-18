import sys
import pandas as pd
import requests
import os
import re
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


session = requests.Session()

# Pass headers
# Sometimes, user agent versions give errors, try changing them if you face errors such as connection aborted
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


def get_ean(soup):
    ean_tag = soup.find('dt', text=re.compile(r'\s*EAN\s*', re.IGNORECASE))
    if ean_tag:
        ean_value = ean_tag.find_next_sibling('dd').text.strip()
        return ean_value
    else:
        return 'EAN not found'


def get_mpn(soup):
    mpn_tag = soup.find('dt', text=re.compile('MPN|Manufacturer', re.IGNORECASE))
    if mpn_tag:
        return mpn_tag.find_next_sibling('dd').text.strip()
    else:
        return 'MPN not found'


def get_amazon_model(soup):
    model_tag = soup.find('span', text=re.compile(r'Modelnummer item\s*', re.IGNORECASE))
    if model_tag:
        model = model_tag.find_next_sibling('span').text.strip()
        return model
    else:
        model_tag = soup.find('th', text=re.compile(r'Model', re.IGNORECASE))
        if model_tag:
            model = model_tag.find_next_sibling('td').text.strip()
            return model
        else:
            return 'Model number not found'


def get_amazon_asin(soup):
    asin_tag = soup.find('span', text=re.compile(r'ASIN\s*', re.IGNORECASE))
    if asin_tag:
        asin = asin_tag.find_next_sibling('span').text.strip()
        return asin
    else:
        asin_tag = soup.find('th', text=re.compile(r'ASIN', re.IGNORECASE))
        if asin_tag:
            asin = asin_tag.find_next_sibling('td').text.strip()
            return asin
        else:
            return 'ASIN not found'


def get_amazon_part_no(soup):
    part_no = soup.find('th', text=re.compile(r'Onderdeelnummer\s*', re.IGNORECASE))
    if part_no:
        return part_no.find_next_sibling('td').text.strip()
    else:
        return 'Part number not found'


data_dir = 'data/clustered'

for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(data_dir, filename)
        df = pd.read_csv(filepath)

        # Create empty columns for EAN and MPN
        ean = []
        mpn = []
        model = []
        asin = []
        partno = []

        for index, row in df.iterrows():
            if row['source'] == 'bol':
                url = row['links']
                session.headers.update(my_headers)
                response = session.get(url)
                # response = requests.get(url, headers=my_headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                # Call the get_ean and get_mpn functions
                ean = get_ean(soup)
                mpn = get_mpn(soup)
                df.at[index, 'ean'] = ean
                df.at[index, 'mpn'] = mpn
                time.sleep(2)
            if row['source'] == 'amazon':
                url = row['links']
                session.headers.update(my_headers)
                response = session.get(url)
                # response = requests.get(url, headers=my_headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                # Call the get_ean and get_mpn functions
                asin = get_amazon_asin(soup)
                model = get_amazon_model(soup)
                partno = get_amazon_part_no(soup)
                df.at[index, 'asin'] = asin
                df.at[index, 'model'] = model
                df.at[index, 'partno'] = partno
                time.sleep(2)

        df['ean'] = ean
        df['mpn'] = mpn
        df['asin'] = asin
        df['model'] = model
        df['partno'] = partno
        df.to_csv(filepath, index=False)
    sys.exit()
