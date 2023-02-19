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
        return {}

def get_all_links_bol(driver, link):
    visited = set()
    next_wave = set([link])
    while next_wave:
        current_wave = next_wave.copy()
        next_wave.clear()
        for current_link in current_wave:
            visited.add(current_link)
            children_links = get_all_links_from_website(driver, current_link)
            for l in children_links:
                if l not in visited:
                    next_wave.add(l)
    return visited

def get_all_links_from_website(driver, link):
    driver.get(link)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "features.js_features"))
        )
    except:
        return [link]
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    lists = get_all_choice_groups(soup)
    links = []
    for l in lists:
        try:
            children = get_all_children_Tags(l)
        except:
            continue
        for child in children:
            child_link = 'https://bol.com'+child.get('href')
            links.append(child_link)
    return links

def get_all_choice_groups(soup):
    el = soup.find("div",{"class": "features js_features"})
    step = get_all_children_Tags(el)
    actual_lists = [get_child_by_data_test(i,'feature-options') for i in step]
    return actual_lists

def get_child_by_data_test(item, term):
    children = item.find_all(recursive=False)
    for child in children:
        if child.get('data-test') == term:
            return child

def get_title_from_element_bol(elem):
    text = str(elem.contents[0])
    return text.strip()


def get_specs_bol_from_rows(rows):
    returner = {}
    for r in rows:
        title_elem, value_elem = r.find_all('div', recursive=False)
        title = title_elem.contents[0].strip()
        value = value_elem.contents[0].strip()
        returner[title] = value
    return returner
