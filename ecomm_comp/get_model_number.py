import pandas as pd
import glob, time
import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

path = "data"
extension = 'csv'

files = glob.glob(path + "/*." + extension)

session = requests.Session()
def get_div(tag,name):
    for child in tag:
        if child.name == name:
            return child
def get_dict_input(tag):
    contents = get_div(tag,'span')
    #initializaiton
    title = 0
    content = 0
    for child in contents:
        if type(child) == Tag:
            if title == 0:
                title = child
            elif content == 0:
                content = child
        else:
            #print(type(child))
            b=2
    title = title.string
    stop = title.find(":")
    title = title[:stop]
    if "\n" in title:
        words = title.split("\n")
        title = words[0]
    content = content.string
    return {title : content}
def handle_amazon(soup):
        div = soup.find(id="detailBullets_feature_div")
        contents = get_div(div, 'div')
        list = get_div(contents, 'div')
        text = get_div(list, 'ul')
        product_details = dict()
        for detail in text.contents:
            if type(detail) == Tag:
                dict_slip = get_dict_input(detail)
                product_details.update(dict_slip)
        print(product_details)
        return product_details

#driver = webdriver.Chrome()
#driver.implicitly_wait(3)
for filename in files:
    # If file(s) found
    if filename:
        df = pd.read_csv(filename, index_col=None)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Get the link column of the file(s)
        links = df.link
        for i in links:
            print(i)

            # Open the link in BS4 and get the details
            # Model number for now and up to 5 images as some model numbers have different last few digits.
            # So, we might have to compare model numbers and images to get the exact match
            # This step can be improved using multithreading


            driver.get(i)
            try:
                elem = WebDriverWait(driver,10).until(
                   EC.presence_of_element_located((By.ID, "detailBullets_feature_div"))
                )
            except:
                print("No product details found")
                continue
            b=2
            html_soup = BeautifulSoup(driver.page_source, 'html.parser')
            soup = BeautifulSoup(str(html_soup), features='lxml')
            # For amazon
            if "amazon" in i:
                try:
                    dictionary = handle_amazon(soup)
                except:
                    b=2
                    dictionary = handle_amazon(soup)

    break

