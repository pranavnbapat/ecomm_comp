import pandas as pd
import glob
from scraping_general import accept_cookies_wrap
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bol_scraping import get_specs_bol, get_all_links_bol
from amazon_scraping import get_specs_amazon, get_all_links
from os.path import exists
import os
path_clustered = "data/clustered"
extension = 'csv'
path_matched = 'data/matched'
os.makedirs(path_matched,exist_ok=True)
files = glob.glob(path_clustered + "/*." + extension)

for filename in files:
    # If file(s) found
    if filename and not exists(filename.replace(path_clustered,path_matched)):
        df = pd.read_csv(filename, index_col=None)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(2)
        accept_cookies_wrap(driver)
        # Get the link column of the file(s)
        links = df.links
        bol_model = {}
        amazon_model = {}
        accept_cookies_wrap(driver)
        already_visited = set()
        for i in links:
            if i == "No link found" or i in already_visited:
                continue
            if "amazon" in i:
                    all_links = get_all_links(driver, i)
                    already_visited.update(all_links)
                    for l in all_links:
                        specs = get_specs_amazon(driver, l)
                        if "Modelnummer item" in specs:
                            amazon_model[(specs.get("Modelnummer item"))] = l
            elif "bol" in i:
                links = get_all_links_bol(driver,i)
                already_visited.update(links)
                for l in links:
                    specs = get_specs_bol(driver, l)
                    if "MPN (Manufacturer Part Number)" in specs:
                        bol_model[(specs.get("MPN (Manufacturer Part Number)"))] = i

        match = [i for i in list(bol_model.keys()) if i in list(amazon_model.keys())]
        reverse_match = [i for i in list(bol_model.keys()) if i not in match]
        reverse_match = [bol_model.get(i) for i in reverse_match]

        csv_data = []
        for m in match:
                csv_data.append([bol_model.get(m),amazon_model.get(m)])
        df = pd.DataFrame(data=csv_data,columns=["Bol link","Amazon link"])
        df.to_csv(filename.replace(path_clustered,path_matched),index=False)
        #df_reverse = pd.DataFrame(data = reverse_match,columns=["Failed_links"])
        #df_reverse.to_csv(filename.replace(".csv","_failed_matchings.csv"),index=False)
        print(f"{len(match)} MATCHES FROM {len(bol_model)} BOL MODELS AND {len(amazon_model)}  AMAZON MODELS")
        driver.close()

