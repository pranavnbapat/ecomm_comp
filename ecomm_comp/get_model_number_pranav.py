import pandas as pd
import glob
from scraping_general import accept_cookies_wrap
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bol_scraping import get_specs_bol, get_all_links_bol
from amazon_scraping import get_specs_amazon, get_all_links

path = "data/clustered"
extension = 'csv'

files = glob.glob(path + "/*." + extension)

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.implicitly_wait(2)
    accept_cookies_wrap(driver)
    for filename in files:
        # If file(s) found
        if filename:
            df = pd.read_csv(filename, index_col=None)
            # Get the link column of the file(s)
            links = df.links
            bol_model = {}
            amazon_model = {}
            for i in links:
                if i == "No link found":
                    continue
                if "amazon" in i:
                    all_links = get_all_links(driver, i)
                    for l in all_links:
                        specs = get_specs_amazon(driver, l)
                        if "Modelnummer item" in specs:
                            amazon_model[(specs.get("Modelnummer item"))] = l
                elif "bol" in i:
                    links = get_all_links_bol(driver, i)
                    for l in links:
                        specs = get_specs_bol(driver, l)
                        if "MPN (Manufacturer Part Number)" in specs:
                            bol_model[(specs.get("MPN (Manufacturer Part Number)"))] = i

            # Convert the matching and reverse matching to sets
            bol_set = set(bol_model.items())
            amazon_set = set(amazon_model.items())
            match_set = bol_set & amazon_set
            reverse_match_set = bol_set - amazon_set

            # Convert the sets back to lists for creating the dataframes
            match_list = [[m[1], amazon_model.get(m[0])] for m in match_set]
            reverse_match_list = [b[1] for b in reverse_match_set]

            # Create a single dataframe for both matches and reverse matches
            df = pd.DataFrame(data=match_list, columns=["Bol link", "Amazon link"])
            df_reverse = pd.DataFrame(data=reverse_match_list, columns=["Failed_links"])
            combined_df = pd.concat([df, df_reverse], ignore_index=True, axis=1)

            # Write the dataframe to a new file
            combined_df.to_csv(filename.replace(".csv", "_matchings.csv"), index=False)
            print(f"{len(match_set)} MATCHES FROM {len(bol_set)} BOL MODELS AND {len(amazon_set)} AMAZON MODELS")