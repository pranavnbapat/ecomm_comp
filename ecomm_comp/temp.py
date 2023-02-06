import sys
import time
import pandas as pd
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from core_functions import my_headers
from pathlib import Path

brand = "samsung"
search_term = f"{brand} smartwatch"


def check_words_in_string(string, words_to_check):
    words = string.split(" ")
    for w in words_to_check:
        if w not in words:
            return False
    return True


# Creating a session object for each iteration is resource-intensive and time-consuming.
# By moving the session object outside of the for loop, you can reuse the same session object for multiple
# requests and improve performance.
session = requests.Session()

prices = []
products = []
source = []
timestamp = []
links = []

# toolbar_width = 40
# sys.stdout.write("[%s]" % (" " * toolbar_width))
# sys.stdout.flush()
# sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
# for i in range(toolbar_width):

for i in range(1, 201):
    url = f"https://www.bol.com/nl/nl/s/?searchtext={search_term}&page={i}"
    response = session.get(url, headers=my_headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup.find_all("div", attrs={"class": "product-item__content"}):
        product_price = tag.find("div", attrs={"class": "price-block__highlight"})
        # for product_price in tag.find("div", attrs={"class": "price-block__highlight"}):
        if product_price:
            product = tag.find("a", attrs={"class": "product-title"}).get_text().encode("ascii", "ignore").decode(
                "utf-8")
            prices.append(str(product_price.get_text()))

            products.append(product)
            source.append("bol")
            timestamp.append(str(datetime.now()))
            for link in tag.find_all("a", attrs={"class": "product-title"}):
                links.append("https://bol.com" + link['href'])
    time.sleep(2)


print(len(prices))
print(len(source))
print(len(timestamp))
print(len(products))
print(len(links))


for i in range(1, 20):
    url = f"https://www.amazon.nl/s?k={re.sub(' ', '+', search_term)}&page={i}"
    response = session.get(url, headers=my_headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for tag in soup.find_all("div", attrs={"data-component-type": "s-search-result"}):
        if tag.find("span", attrs={"class": "a-price-whole"}):
            price = tag.find("span", attrs={"class": "a-price-whole"}).get_text()
            if price:
                prices.append(str(price))
                source.append("amazon")
                product = tag.find("h2",
                                   attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-4"}).get_text()\
                    .encode("ascii", "ignore").decode("utf-8")
                products.append(product)

                # For product link
                for product_link in tag.find_all("a", attrs={"class": "a-link-normal s-no-outline"}):
                    links.append("https://www.amazon.nl" + product_link['href'])

                # Get current timestamp
                timestamp.append(str(datetime.now()))

print(len(prices))
print(len(source))
print(len(timestamp))
print(len(products))
print(len(links))

df = pd.DataFrame(columns=["products", "prices", "source", "timestamp", "links"])
pd.to_datetime(df.timestamp, format="%Y-%m-%d %H:%M:%S")
df['products'] = products
df['products'] = df['products'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

df['prices'] = prices
df['prices'] = df['prices'].apply(lambda x: re.sub(r'[^\d.,]', '', x).replace(r'(\.){2,}', '.', x))


df['links'] = links
df['source'] = source
df['timestamp'] = timestamp
Path("data").mkdir(parents=True, exist_ok=True)
df.to_csv(f"data/{search_term}_{str(datetime.now()).replace(':', '_').split('.', 1)[0]}.csv", index=False)
print("Results saved to CSV file inside 'data' folder")
