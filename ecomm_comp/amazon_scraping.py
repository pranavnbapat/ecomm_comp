from bs4 import Tag, BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scraping_general import get_child, get_child_Tag, get_all_children_Tags, get_all_child_by_name
import time


def handle_amazon(soup):
    # Finds product details
    div = soup.find(id="detailBullets_feature_div")
    contents = get_child(div, 'div')
    list = get_child(contents, 'div')
    text = get_child(list, 'ul')
    # After a bit of a digging
    product_details = dict()
    for detail in text.contents:
        if type(detail) == Tag:
            # Extracts the dictionary matching
            dict_slip = get_dict_input(detail)
            product_details.update(dict_slip)
    return product_details


def get_specs_amazon(driver, link):
    # Main method to get the specifications
    # Runs a side method handle_amazon after waiting for the product details to load
    driver.get(link)
    try:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "detailBullets_feature_div"))
        )
    except:
        # print("No product details found")
        return {}
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    try:
        dictionary = handle_amazon(soup)
        return dictionary
    except:
        return {}


def get_all_lists(soup):
    # This complicated method finds the actual list of buttons on the website.
    # Because of IDK what, the sites can have different structure, but from experience this method
    # Covers all of the possibilities
    div = soup.find(id="twister_feature_div")
    lists = div.find(id="twister-plus-inline-twister-container")
    if lists:
        deeper_lists = lists.find(id="twister-plus-inline-twister-card")
        even_deeper = get_child_Tag(get_child_Tag(deeper_lists))
        lists = get_all_children_Tags(even_deeper)
        return lists
    else:
        deeper_lists = div.find(id="twister-plus-inline-twister")
        if deeper_lists:
            lists = get_all_children_Tags(deeper_lists)
            return lists
        else:
            deeper_lists = div.find(id="twister")
            if deeper_lists:
                return get_all_child_by_name(deeper_lists, 'div')
            else:
                return False


def get_all_clickables(l):
    # Again, a lot of digging as the actual elements are buried
    # Gets the actual button elements in the list of buttons
    # Returns the id's of the button elements
    # We need the id's to alter search for them with selenum and click them
    one_step = get_child(l, 'div')
    two_step = get_child(one_step, 'div')
    if two_step:
        three_step = get_child(two_step, 'div')
        fourth_step = get_child(three_step, 'ul')
        fifth_step = get_all_children_Tags(fourth_step)
        all_ids = list()
        for i in fifth_step:
            att = i.attrs
            if 'data-asin' in att:
                one_deep = get_child(i, 'span')
                two_deep = get_child(one_deep, 'span')
                all_ids.append(two_deep.get('id'))
        return all_ids
    else:
        one_step = get_child(l, 'ul')
        if one_step:
            two_step = get_all_children_Tags(one_step)
            all_ids = list()
            for tag in two_step:
                all_ids.append(tag.get('id'))
            return all_ids
        else:
            return False


def try_clicking(button, retry=0):
    # Wrapper for clicking, sometimes shit didnt work cause it was blocked by another element of page
    if retry == 3:
        return
    else:
        try:
            button.click()
        except:
            try_clicking(button, retry + 1)


def get_all_link_combinations(driver, click_ids, num, max, past_clicks=None):
    # BFS big method for getting all of the combinations
    # Goes down the click_ids, which is a list of lists of button ids to press
    # At each tree step it picks a list of buttons to click from

    # It only clicks all the button at the last step ( last list of buttons), as sometimes clicking a button
    # Changes more than 1 thing( like u click a color button and size changes cause it wasnt available)
    # Because of that at last step we check if buttons are available in the current option we have

    # As an example of how it works more or less:

    # Lets say we have in click_ids ids for buttons for size and color
    # First it looks at size options, locks down size 40mm
    # When it arrives at the last choice, it checks all the button availabilities
    # Only clicks the available ones for the last choice
    # Which saves a lot of clicking
    # Then goes to size 44mm and repeats

    if past_clicks == None:
        past_clicks = list()
    main_links = set()
    if num < max:
        option = click_ids[num]
        for id in option:
            clicked = list()
            for item in past_clicks:
                clicked.append(item)
            button = driver.find_element('id', id)
            clicked.append(button)
            links_from_child = get_all_link_combinations(driver, click_ids, num + 1, max, clicked)
            main_links.update(links_from_child)
        return main_links
    else:
        for past_button in past_clicks:
            try_clicking(past_button)
        html_soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = BeautifulSoup(str(html_soup), features='lxml')
        option = click_ids[max]
        time.sleep(2)
        for id in option:
            el = soup.find(id=id)
            availability = el.get('class')[0]
            if "Unavailable" not in availability:
                button = driver.find_element('id', id)
                try_clicking(button)
                time.sleep(2)
                url = str(driver.current_url)
                main_links.add(url)
        return main_links


def get_all_links(driver, link):
    # Gets all available links from the main link site
    # On amazon all the options are immediately shown, so bol and amazon have different approaches
    driver.get(link)
    driver.fullscreen_window()
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "twister_feature_div"))
        )
    except:
        # print("No extra links found")
        return [link]
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = BeautifulSoup(str(html_soup), features='lxml')
    lists = get_all_lists(soup)
    if lists == False:
        return [link]
    click_ids = []
    for l in lists:
        click_ids.append(get_all_clickables(l))
    click_ids = [i for i in click_ids if i is not False]
    if len(click_ids) == 0:
        return [link]
    else:
        click_ids.sort(key=len)
        final_links = get_all_link_combinations(driver, click_ids, 0, len(click_ids) - 1)
        # print(len(final_links))
        return final_links


def get_dict_input(tag):
    # Transforms an element of product specs into dictionary input ( term : value)
    contents = get_child(tag, 'span')
    title = 0
    content = 0
    for child in contents:
        if type(child) == Tag:
            if title == 0:
                title = child
            elif content == 0:
                content = child
    title = title.string
    stop = title.find(":")
    title = title[:stop]
    if "\n" in title:
        words = title.split("\n")
        title = words[0]
    content = content.string
    return {title: content}
