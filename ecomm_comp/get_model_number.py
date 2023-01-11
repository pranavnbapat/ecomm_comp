import pandas as pd
import glob
import requests
from bs4 import BeautifulSoup

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

for filename in files:
    # If file(s) found
    if filename:
        df = pd.read_csv(filename, index_col=None)

        # Get the link column of the file(s)
        links = df.link
        for i in links:
            print(i)
            # Open the link in BS4 and get the details
            # Model number for now and up to 5 images as some model numbers have different last few digits.
            # So, we might have to compare model numbers and images to get the exact match
            # This step can be improved using multithreading
            response = session.get(i, headers=my_headers)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            soup = BeautifulSoup(str(html_soup), features='lxml')
            # For amazon
            for model_no in soup.find_all(
                    'ul',
                    attrs={
                        "class": "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}
            ):
                print(model_no)

            # Once details are retrieved, update the same CSV file with the new details

    break

