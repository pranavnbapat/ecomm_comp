import time
from tqdm import tqdm
import pandas as pd
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from ecomm_comp.old_files.core_functions import my_headers
from pathlib import Path
import deepl

auth_key = "d35a289e-47d2-a38e-09a7-f0de53284a56:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

brand = "apple"
search_term = f"{brand} smartwatch"


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
start_time = time.time()
for i in tqdm(range(1, 11)):
    try:
        url = f"https://www.bol.com/nl/nl/s/?searchtext={search_term}&page={i}"
        response = session.get(url, headers=my_headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all("div", attrs={"class": "product-item__content"}):
            product_price = tag.find("div", attrs={"class": "price-block__highlight"})
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
    except Exception as e:
        print(e)
# time.sleep(0.1)

for i in tqdm(range(1, 21)):
    try:
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
    except Exception as e:
        print(e)
    time.sleep(0.1)

print(f"Performing data cleaning operations...")
df = pd.DataFrame(columns=["products", "prices", "source", "timestamp", "links"])
pd.to_datetime(df.timestamp, format="%Y-%m-%d %H:%M:%S")
df['products'] = products
# Strip leading and trailing whitespaces
df['products'] = df['products'].str.strip()
# Remove punctuations
df['products'] = df['products'].apply(lambda x: re.sub(r'[^\w\s]', '', x))

df['prices'] = prices
# Strip leading and trailing whitespaces
df['prices'] = df['prices'].str.strip()
# Replace commas with periods
df['prices'] = df['prices'].apply(lambda x: re.sub(",-", "", re.sub(" +", ",", re.sub("\n", "", str(x)))))
df['prices'] = df['prices'].apply(lambda x: re.sub(r',', '.', str(x)))
df['prices'] = df['prices'].astype(float)
df['prices'] = df['prices'].round(2)

df['links'] = links
df['source'] = source
df['timestamp'] = timestamp

# Drop if brand name is not present
df = df[df.products.str.contains(brand, case=False)]

# Drop duplicates
df = df.drop_duplicates(subset='products', keep="first")

# Translate to English
translated = []
for index, value in df.iterrows():
    # Clean the data by changing apple watch4 to apple watch 4 and watch5 40mm to watch 5 40 mm, etc.
    output = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', value["products"])
    output = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', output)
    translated.append(translator.translate_text(output, target_lang="EN-GB"))
df["products"] = translated

Path("../data").mkdir(parents=True, exist_ok=True)
df.to_csv(f"data/{search_term.replace(' ', '_')}_{str(datetime.now()).replace(':', '_').split('.', 1)[0]}.csv",
          index=False)
print("Results saved to CSV file inside 'data' folder")
print("--- %s seconds ---" % (time.time() - start_time))
