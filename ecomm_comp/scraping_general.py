from bs4 import Tag
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# I hope this is self-explanatory
def get_child_Tag(element):
    for child in element.contents:
        if type(child) == Tag:
            return child
    return None


def get_all_children_Tags(element):
    tags = list()
    for child in element.contents:
        if type(child) == Tag:
            tags.append(child)
    return tags


def get_all_child_by_name(element, name):
    tags = list()
    for child in element.contents:
        if child.name == name:
            tags.append(child)
    return tags


def get_child(tag, name):
    for child in tag:
        if child.name == name:
            return child
    return None


def accept_cookie(driver, link, id):
    driver.get(link)
    try:
        elem = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, id))
        )
        elem.click()
    except:
        print("we in")


def accept_cookies_wrap(driver):
    accept_cookie(driver,
                  "https://www.amazon.nl/Samsung-Galaxy-Watch-Classic-Bluetooth/dp/B099SF8DWX/ref=sr_1_3?qid=1673621019&refinements=p_89%3Asamsung&s=electronics&sr=1-3",
                  "sp-cc-accept")
    accept_cookie(driver,
                  "https://bol.com/nl/nl/p/samsung-galaxy-watch4-classic-smartwatch-zwart-staal-46mm/9300000108147961/",
                  "js-first-screen-accept-all-button")
