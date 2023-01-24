from scraping_general import get_child, get_all_children_Tags
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_specs_bol(driver, link):
    driver.get(link)
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "specs__list"))
        )
    except:
        print("Could not find product information for this link")
        return {}
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    mydivs = soup.find_all("div", {"class": "specs"})
    main_list = False
    for div in mydivs:
        if "Productinformatie" in div.text:
            main_list = div
            break
    if main_list:
        list = get_child(main_list, "dl")
        all_rows = get_all_children_Tags(list)
        return get_specs_bol_from_rows(all_rows)
    else:
        print("Could not find product information for this link")
        return {}


def get_title_from_element_bol(elem):
    text = str(elem.contents[0])
    return text.strip()


def get_specs_bol_from_rows(rows):
    returner = {}
    for r in rows:
        title_elem = get_child(r, 'dt')
        value_elem = get_child(r, 'dd')
        title = get_title_from_element_bol(title_elem)
        value = get_title_from_element_bol(value_elem)
        returner[title] = value
    return returner
