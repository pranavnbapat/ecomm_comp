import os
import shutil
import sys
import time
import urllib
import urllib.request
import re
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

amazon_api = os.getenv('amazon_smartwatch')
bol_api = os.getenv('bol_smartwatch')


def extract_data_from_html(filename):
    soup = BeautifulSoup(open("temp_data/" + filename), "html.parser")
    return soup


def scrape_data():
    page = 1
    product_names_list = []
    product_prices_list = []
    product_link_list = []
    product_source_list = []

    # Pass headers
    my_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
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
    session = requests.Session()

    try:
        while page != 400:
            # Build URL
            amazon_url = amazon_api + str(page)

            response = session.get(amazon_url, headers=my_headers)

            html_soup = BeautifulSoup(response.text, 'html.parser')

            soup = BeautifulSoup(str(html_soup), features='lxml')

            product_info = soup.find_all("div", attrs={"data-component-type": "s-search-result"})

            for temp in product_info:
                # Check if price exists
                if temp.find("span", attrs={"class": "a-price-whole"}):
                    # For product price
                    for price in temp.find_all("span", attrs={"class": "a-price-whole"}):
                        product_prices_list.append(price.get_text())
                        product_source_list.append("Amazon")

                    # For product name
                    for product_name in temp.find_all("div", attrs={
                        "class": "a-section a-spacing-none a-spacing-top-small s-title-instructions-style"
                    }):
                        for product_name2 in product_name.find_all("h2"):
                            product_names_list.append(product_name2.get_text())

                    # For product link
                    for product_link in temp.find_all("a", attrs={"class": "a-link-normal s-no-outline"}):
                        product_link_list.append("https://www.amazon.nl" + product_link['href'])

            page = page + 1
    except Exception as e:
        print(e)

    page = 1

    try:
        while page != 100:
            # Build URL
            bol_url = bol_api + str(page)

            response = session.get(bol_url, headers=my_headers)

            html_soup = BeautifulSoup(response.text, 'html.parser')

            soup = BeautifulSoup(str(html_soup), features='lxml')

            product_info = soup.find_all("ul", attrs={"class": "list-view product-list js_multiple_basket_buttons_page"})
            for temp in product_info:
                # Check if price exists
                if temp.find("div", attrs={"class": "price-block__price"}):
                    # For product price
                    for product_price in temp.find_all("div", attrs={"class": "price-block__price"}):
                        product_prices_list.append(
                            re.sub(",-", "", re.sub(" +", ",", re.sub("\n", "", str(product_price.get_text())).strip()))
                        )
                        product_source_list.append("BOL")

                    # For product name
                    for product_name in temp.find_all("div", attrs={"class": "product-title--inline"}):
                        product_names_list.append(product_name.get_text())

                    # For product link
                    for product_link in temp.find_all("a", attrs={
                        "class": "product-title px_list_page_product_click list_page_product_tracking_target"
                    }):
                        product_link_list.append(product_link['href'])

            page = page + 1
            time.sleep(10)
    except Exception as e:
        print(e)

    return product_names_list, product_prices_list, product_link_list, product_source_list


if __name__ == "__main__":
    product = "smartwatch"
    # brand_list = ["samsung", "apple", "xiaomi", "fitbit sense", "garmin", "popglory", "huawei", "dachma", "nintendo",
    #               "lige", "agptek", "pthtechus", "nuvance", "motivo", "amzsa", "miclee", "yonmig", "pop glory"]

    # Getting data
    df = pd.DataFrame(columns=["product", "price", "link", "source"])
    product_list, price_list, link_list, source_list = scrape_data()

    # Getting brand
    # temp_list = []
    # for x in product_list:
    #     for y in brand_list:
    #         if re.search(y, x, re.IGNORECASE):
    #             temp_list.append(y)
    #
    # print(temp_list)
    # print(len(temp_list))

    df['product'] = product_list
    df['price'] = price_list
    df['source'] = source_list
    df['link'] = link_list

    df.to_csv("smartwatch.csv", index=False, encoding='utf-8')
