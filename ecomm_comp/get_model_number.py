import pandas as pd
import glob, time
import requests, copy
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
    return None
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
def get_specs(driver,link):
    driver.get(link)
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "detailBullets_feature_div"))
        )
    except:
        print("No product details found")
        return {}
    b = 2
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    # For amazon
    if "amazon" in i:
        try:
            dictionary = handle_amazon(soup)
        except:
            b = 2
            return {}
            #dictionary = handle_amazon(soup)
    else:
        print("BOL NOT YET IMPLEMENTED")
        return {}
    return dictionary
def get_child_Tag(element):
    for child in element.contents:
        if type(child) == Tag:
            return child
    return None
def get_all_children_Tags(element):
    tags=list()
    for child in element.contents:
        if type(child) == Tag:
            tags.append(child)
    return tags
def get_all_child_by_name(element,name):
    tags = list()
    for child in element.contents:
        if child.name == name:
            tags.append(child)
    return tags
def get_all_lists(soup):
    div = soup.find(id="twister_feature_div")
    lists = div.find(id="twister-plus-inline-twister-container")
    if lists:
        deeper_lists = lists.find(id="twister-plus-inline-twister-card")
        even_deeper = get_child_Tag(get_child_Tag(deeper_lists))
        lists= get_all_children_Tags(even_deeper)
        return lists
    else:               # THE WEBSITES FOLLOWS PRETTY MUCH 3 STRUCTURES, FROM EXPERIENCE THIS COVERS ALL
        deeper_lists = div.find(id="twister-plus-inline-twister")
        if deeper_lists:
            lists=get_all_children_Tags(deeper_lists)
            return lists
        else:
            deeper_lists = div.find(id="twister")

            return get_all_child_by_name(deeper_lists,'div')
def get_all_clickables(l):
    one_step = get_div(l,'div')
    two_step = get_div(one_step,'div')
    if two_step:
        three_step = get_div(two_step,'div')
        fourth_step = get_div(three_step,'ul')
        fifth_step = get_all_children_Tags(fourth_step)
        all_ids = list()
        for i in fifth_step:
            att = i.attrs
            if 'data-asin' in att:
                one_deep = get_div(i,'span')
                two_deep = get_div(one_deep,'span')
                all_ids.append(two_deep.get('id'))
        return all_ids
    else:
        one_step = get_div(l,'ul')
        two_step = get_all_children_Tags(one_step)
        all_ids = list()
        for tag in two_step:
            all_ids.append(tag.get('id'))
        return all_ids


def get_all_link_combinations(driver,click_ids,num,max,past_clicks=list()):
    main_links = set()
    clicked = copy.copy(past_clicks)
    if num<max:
        option = click_ids[num]
        for id in option:
            button = driver.find_element('id',id)
            clicked.append(button)
            driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
            links_from_child = get_all_link_combinations(driver,click_ids,num+1,max,clicked)
            main_links.update(links_from_child)
        return main_links
    else:
        option = click_ids[max]
        for id in option:
            for past_button in clicked:
                driver.execute_script("arguments[0].scrollIntoView();", past_button)
                past_button.click()

                """
                The above step is quite crucial
                example options
                
                GPS     GPS+LTE
                
                GOOD   BAD
                
                BLACK RED YELLOW
                
                
                You go GPS -> Good -> colors
                But Yellow is only available on GPS+LTE
                After all colors, you click BAD and go all colors
                But since you clicked yellow, GPS+LTE was clicked automatically by amazon
                Therefore locking us out of GPS -> BAD -> BLACK, RED
                """
            button = driver.find_element('id', id)
            driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
            time.sleep(2.5)
            url = str(driver.current_url)
            main_links.add(url)
        return main_links

def get_all_links(driver,link):
    driver.get(link)
    driver.fullscreen_window()
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twister_feature_div"))
        )
    except:
        print("No extra links found")
        return [link]
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    lists = get_all_lists(soup)
    click_ids=[]
    for l in lists:
        click_ids.append(get_all_clickables(l))
    final_links = get_all_link_combinations(driver,click_ids,0,len(click_ids)-1)
    print(len(final_links))





    """
   DIV IDS CONTAINIGN CHOCIES
   
   twister_feature_div  # SEEMS TO WORK FOR ALL
    twister-plus-inline-twister  # THIS ONE ON OPERA
    """
#driver = webdriver.Chrome()
#driver.implicitly_wait(3)
for filename in files:
    # If file(s) found
    if filename:
        df = pd.read_csv(filename, index_col=None)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(2)
        # Get the link column of the file(s)
        links = df.link
        for i in links:
            print(i)
            if "amazon" in i:
                get_all_links(driver,i)
            # Open the link in BS4 and get the details
            # Model number for now and up to 5 images as some model numbers have different last few digits.
            # So, we might have to compare model numbers and images to get the exact match
            # This step can be improved using multithreading


    break

