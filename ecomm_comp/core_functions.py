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

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))


load_dotenv()

amazon_api = os.getenv('amazon_smartwatch')
bol_api = os.getenv('bol_smartwatch')


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


# Flattening lists function
def flatten_list(lis):
    try:
        for item in lis:
            if isinstance(item, cl.Iterable) and not isinstance(item, str):
                for x in flatten_list(item):
                    yield x
            else:
                yield item
    except Exception as e:
        print(e)


def scrape_amazon(brand):
    print("Scraping amazon.nl...")

    session = requests.Session()

    # amazon.nl
    page = 1
    amazon_product_names_list = []
    amazon_product_prices_list = []
    amazon_product_link_list = []
    amazon_product_source_list = []
    amazon_timestamp_list = []

    try:
        while page != 10:
            # Build URL
            amazon_url = amazon_api + brand + "&page=" + str(page)

            response = session.get(amazon_url, headers=my_headers)

            html_soup = BeautifulSoup(response.text, 'html.parser')

            soup = BeautifulSoup(str(html_soup), features='lxml')

            product_info = soup.find_all("div", attrs={"data-component-type": "s-search-result"})

            for temp in product_info:
                i = 1
                # Get the record only if price exists
                if temp.find("span", attrs={"class": "a-price-whole"}):
                    # For product price
                    for price in temp.find("span", attrs={"class": "a-price-whole"}):
                        amazon_product_prices_list.append(price.get_text())
                        amazon_product_source_list.append("amazon")

                    # For product name
                    for product_name in temp.find_all(
                            "h2",
                            attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-4"}
                    ):
                        # for product_name2 in product_name.find_all("h2"):
                        amazon_product_names_list.append(product_name.get_text())

                    # For product link
                    for product_link in temp.find_all("a", attrs={"class": "a-link-normal s-no-outline"}):
                        amazon_product_link_list.append("https://www.amazon.nl" + product_link['href'])

                    # Get current timestamp
                    timestamp = datetime.now()
                    amazon_timestamp_list.append(timestamp)

                i = i + 1
            page = page + 1
    except Exception as e:
        print(e)

    print("Scraping finished! Total " + str(len(amazon_product_names_list)) + " products found.\n")

    return amazon_product_names_list, amazon_product_prices_list, amazon_product_link_list, \
        amazon_product_source_list, amazon_timestamp_list


def scrape_bol(brand):
    print("Scraping bol.com...")

    session = requests.Session()

    # bol.com
    page = 1
    bol_product_names_list = []
    bol_product_prices_list = []
    bol_product_link_list = []
    bol_product_source_list = []
    bol_timestamp_list = []

    try:
        while page != 100:
            # Build URL
            bol_url = bol_api + str(page)

            response = session.get(bol_url, headers=my_headers)

            html_soup = BeautifulSoup(response.text, 'html.parser')

            soup = BeautifulSoup(str(html_soup), features='lxml')

            product_info = soup.find_all("li",
                                         attrs={"class": "product-item--row js_item_root"})

            for temp in product_info:
                # Check for brand name
                if brand == str(temp.find("a", attrs={"data-test": "party-link"}).get_text()).lower():
                    # Get the record only if price exists
                    if temp.find("div", attrs={"class": "price-block__price"}) and \
                            temp.find("div", attrs={"class": "product-title--inline"}):
                        # For product price
                        for product_price in temp.find_all("div", attrs={"class": "price-block__price"}):
                            bol_product_prices_list.append(
                                re.sub(",-", "",
                                       re.sub(" +", ",", re.sub("\n", "", str(product_price.get_text())).strip()))
                            )
                            bol_product_source_list.append("bol")

                        # For product name
                        for product_name in temp.find_all("div", attrs={"class": "product-title--inline"}):
                            bol_product_names_list.append(product_name.get_text())

                        # For product link
                        if temp.find_all("a", attrs={
                            "class": "product-title px_list_page_product_click list_page_product_tracking_target"
                        }):
                            for product_link in temp.find_all("a", attrs={
                                "class": "product-title px_list_page_product_click list_page_product_tracking_target"
                            }):
                                bol_product_link_list.append("https://bol.com" + product_link['href'])
                        else:
                            bol_product_link_list.append("No link found")

                        # Get timestamp
                        timestamp = datetime.now()
                        bol_timestamp_list.append(timestamp)

            page = page + 1
            time.sleep(1)
    except Exception as e:
        print(e)

    print("Scraping finished! Total " + str(len(bol_product_names_list)) + " products found.\n")

    return bol_product_names_list, bol_product_prices_list, bol_product_link_list, bol_product_source_list, \
        bol_timestamp_list


def save_data(product_list, price_list, link_list, source_list, timestamp_list, brand_name):
    print("Saving data to CSV file...")

    try:
        # Create empty dataframe
        df = pd.DataFrame(columns=["product", "price", "source", "timestamp"])
        pd.to_datetime(df.timestamp, format="%Y%m%d%H%M%S")

        # List that we get from scrape_data function is nested. Thus, we need to flatten it
        product_list = list(flatten_list(product_list))
        price_list = list(flatten_list(price_list))
        link_list = list(flatten_list(link_list))
        source_list = list(flatten_list(source_list))
        timestamp_list = list(flatten_list(timestamp_list))

        df['product'] = product_list
        df['price'] = price_list
        df['link'] = link_list
        df['source'] = source_list
        df['timestamp'] = timestamp_list

        # DATA CLEANING
        # Remove new lines
        df['product'] = df['product'].apply(lambda x: re.sub(r"\\n", " ", str(x)).strip())

        # Remove punctuations
        df['product'] = df['product'].apply(lambda x: re.sub(r'[.,$!_\\?/%()\-\"\']+', '', str(x)).strip())

        # Remove stopwords

        # Replace , with . and standardise all values
        df['price'] = df['price'].astype(str)
        df['price'] = df['price'].apply(lambda x: x.replace(',', '.'))
        df['price'] = df['price'].astype(float)
        df['price'] = df['price'].round(2)

        # Save CSV
        Path("data").mkdir(parents=True, exist_ok=True)
        df.to_csv(
            "data/smartwatch_" + brand_name + "_" +
            str(datetime.now()).replace(":", "_").replace("-", "_").split(".", 1)[0] + ".csv",
            index=False, encoding='utf8'
        )
        print("Results saved to CSV file inside 'data' folder")

    except Exception as e:
        print(e)
        print("Exiting. Cannot save data!")
