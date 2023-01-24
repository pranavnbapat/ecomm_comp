import pandas as pd
import glob
from scraping_general import accept_cookies_wrap
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bol_scraping import get_specs_bol
from amazon_scraping import get_specs_amazon, get_all_links

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

for filename in files:
    # If file(s) found
    if filename:
        df = pd.read_csv(filename, index_col=None)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(2)
        accept_cookies_wrap(driver)
        # Get the link column of the file(s)
        links = df.link
        bol_model = []
        amazon_model = []
        for i in links:
            print(i)
            if i == "No link found":
                continue
            if "amazon" in i:
                try:
                    all_links = get_all_links(driver, i)
                    for l in all_links:
                        specs = get_specs_amazon(driver, l)
                        if "Modelnummer item" in specs:
                            amazon_model.append(specs.get("Modelnummer item"))
                except:
                    print("Selenium ran out of memory, restarting browser, skipping link")
                    driver.quit()
                    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                    driver.implicitly_wait(2)
                    accept_cookies_wrap(driver)
            elif "bol" in i:
                specs = get_specs_bol(driver, i)
                if "MPN (Manufacturer Part Number)" in specs:
                    bol_model.append(specs.get("MPN (Manufacturer Part Number)"))

        match = [i for i in bol_model if i in amazon_model]
        print(match)
        print(f"{len(match)} MATCHES FROM {len(bol_model)} BOL MODELS AND {len(amazon_model)}  AMAZON MODELS")

    break
