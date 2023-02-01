from scraping_general import get_child, get_all_children_Tags
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

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
def get_all_links_bol(driver, link):
    visited=list()
    start_links = get_all_links_from_website(driver,link)
    next_wave=start_links
    while next_wave:
        current_wave = list(set(next_wave))
        next_wave = list()
        for linker in current_wave:
            visited.append(linker)
        for current_link in current_wave:
            #print(current_link)
            his_children = get_all_links_from_website(driver,current_link)
            for l in his_children:
                if l not in visited:
                    next_wave.append(l)

    return visited
def get_all_links_from_website(driver,link):
    driver.get(link)
    # driver.fullscreen_window()
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "features.js_features"))
        )
    except:
        print("No extra links found")
        return [link]
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    lists = get_all_choice_groups(soup)
    links=list()
    for l in lists:
        try:
            children = get_all_children_Tags(l)
        except:
            continue
        for child in children:
            child_link = 'https://bol.com'+child.get('href')
            links.append(child_link)
    return links
def get_all_link_combinations(driver,lists,num,max,past_clicks=None):
    if past_clicks == None:
        past_clicks = list()
    main_links = set()
    if num < max:
        option = lists[num]
        for id in option:
            clicked = list()
            for item in past_clicks:
                clicked.append(item)
            button = driver.find_element('id', id)
            clicked.append(button)
            links_from_child = get_all_link_combinations(driver, lists, num + 1, max,clicked)
            main_links.update(links_from_child)
        return main_links
    else:
        #html_soup = BeautifulSoup(driver.page_source, 'html.parser')
        #soup = BeautifulSoup(str(html_soup), features='lxml')
        option = lists[max]
        time.sleep(2)
        for id in option:
            #el = soup.find(id=id)
          #  availability = el.get('class')[0]
           # if "Unavailable" not in availability:
             #   button = driver.find_element('id', id)
            #    try_clicking(button)
             #   time.sleep(2)
            for butt in past_clicks:
                butt.click()
            id.click()
            time.sleep(2)
            url = str(driver.current_url)
            main_links.add(url)
        return main_links
def get_all_choice_groups(soup):
    el = soup.find("div",{"class": "features js_features"})
    step = get_all_children_Tags(el)
    actual_lists = [get_child_by_data_test(i,'feature-options') for i in step]
    return actual_lists

def get_child_by_data_test(item,term):
    actual_children = get_all_children_Tags(item)
    for child in actual_children:
        if child.get('data-test') == term:
            return child

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
