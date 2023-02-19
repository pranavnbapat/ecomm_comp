from scraping_general import get_child, get_all_children_Tags
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def get_specs_bol(driver, link):
    """
    :param driver: Webdriver
    :param link: page link
    :return: a dictionary of product specifications if exists, else empty dictionary
    """
    driver.get(link)
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "specs__list"))
        )
    except:
        return {}
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    # Get all specs
    mydivs = soup.find_all("div", {"class": "specs"})
    main_list = False
    for div in mydivs:
        # look for the one with the stuff we need
        if "Productinformatie" in div.text:
            main_list = div
            break
    if main_list:
        # If correct specs exist go on and extract them into a dictionary
        list = get_child(main_list, "dl")
        all_rows = get_all_children_Tags(list)
        return get_specs_bol_from_rows(all_rows)
    else:
        return {}

def get_all_links_bol(driver, link):
    """
    A simple bfs approach to explore all button options
    :param driver: WebDriver
    :param link: Main page link
    :return:  All possible unique links achievable by clicking buttons around
    """
    visited = set()
    next_wave = {link}
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
    """
    :param driver:  WebDriver
    :param link: link to a website
    :return: A list of all of the links reachable by all buttons on the page
    """
    driver.get(link)
    try:
        # Waiting for the buttons to appear
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "features.js_features"))
        )
    except:
        return [link]

    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    #Find all button sections
    lists = get_all_choice_groups(soup)

    links = []

    for l in lists:
        try:
            # Get all children, which are tags == unique buttons ( if exists)
            children = get_all_children_Tags(l)
        except:
            continue
        for child in children:
            # Gets all href from buttons and puts them in a list
            child_link = 'https://bol.com'+child.get('href')
            links.append(child_link)
    return links

def get_all_choice_groups(soup):
    """
    :param soup: Page soup
    :return: All of the groups of buttons / choices on the page
    """
    el = soup.find("div",{"class": "features js_features"})
    step = get_all_children_Tags(el)
    actual_lists = [get_child_by_data_test(i,'feature-options') for i in step]
    return actual_lists

def get_child_by_data_test(item, term):
    """
    :param item: Some object from bs4 search
    :param term: Term, which children need to have in their 'data-test' parameter
    :return: First child which has TERM in their 'data-test' parameter
    """
    children = item.find_all(recursive=False)
    for child in children:
        if child.get('data-test') == term:
            return child

def get_title_from_element_bol(elem):
    """
    :param elem: bs4 element
    :return: title of the element literally
    """
    text = str(elem.contents[0])
    return text.strip()


def get_specs_bol_from_rows(rows):
    """
    :param rows:  Rows of specifications
    :return: Dictionary, with specs being nicely saved ( title : value inside of dictionary)
    """
    returner = {}
    for r in rows:
        title_elem, value_elem = r.find_all('div', recursive=False)
        title = title_elem.contents[0].strip()
        value = value_elem.contents[0].strip()
        returner[title] = value
    return returner
