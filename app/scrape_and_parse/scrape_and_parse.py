# Built-in imports
from os import getenv
from time import sleep
from json import loads

# Package imports
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Local imports
from .regex import find_and_remove, regex_in, re_line_with_characters, re_guests, re_three_letter_two_digit_date, re_utc_time, re_utc_and_more
from Event import Event

""" PARSING FUNCTIONS """
def parse_page(driver, logged_in):
    event_container = driver.find_element(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]""")
    raw_events = event_container.find_elements(By.XPATH, "*")
    events = []
    for event in raw_events:
        print("Detected upcoming event in {}!".format("page"))
        raw_data = event.text
        if regex_in(raw_data, re_utc_and_more): # Events with multiple times have multiple entries + one main. This is the main, so skip it
            print("detected main event with times, skipping current")
            continue

        
        
        # find_element doesn't work, perhaps due to grandchild?
        try:
            urls = event.find_elements(By.TAG_NAME, "a")
            url = urls[0].get_attribute("href")
            print(url)
        except IndexError:
            print("No url found")
            url = ""

        lines = raw_data.split("\n")
        try:
            event = Event(lines[1], lines[0], "", url)
            events.append(event)
        except IndexError:
            print("Failed to add event from page")
            print(lines)
    return events

def parse_community(driver, logged_in):
    #print(driver.find_element(By.TAG_NAME,"body").text)
    
    if not logged_in:
        event_container = driver.find_element(By.ID, "upcoming_events_card").find_element(By.TAG_NAME, "table")
        raw_events = event_container.find_elements(By.TAG_NAME, "tr")
    else:
        raw_events = driver.find_elements(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div/div/*""")
        raw_events.pop(0)  # First element is title

    events = []
    for event in raw_events:
        print("Detected upcoming event in {}!".format("community"))
        raw_data = event.text

        (raw_data, date) = find_and_remove(raw_data, re_three_letter_two_digit_date)
        (raw_data, time) = find_and_remove(raw_data, re_utc_time)
        (raw_data, guests) = find_and_remove(raw_data, re_guests)  # Unused
        (raw_data, name) = find_and_remove(raw_data, re_line_with_characters)
        url = event.find_element(By.TAG_NAME, "a").get_attribute("href")

        datetime = date + " " + time
        location = raw_data.replace("\n", " ").strip()

        event = Event(name, datetime, location, url)

        print(event.location)

        events.append(event)
    return events


def read_pages_from_env(replace_locale=True):
    """ LOADING & PARSING PAGES FROM .ENV """
    raw_pages = loads(getenv("pages"))
    pages = []
    for raw_page in raw_pages:
        page_type = raw_page[0].lower().strip()
        url = raw_page[1]

        match page_type:
            case "page":
                func = parse_page
            case "community":
                func = parse_community
            case _:  # Default
                func = parse_page
    
        if replace_locale:
            # Specify localisation
            url = url.replace("www.facebook", "en-gb.facebook")

        pages.append((func, url))
    return pages


def scrape_events(driver, pages, logged_in):
    """ RUNNING PARSE FUNCTIONS ON PAGES """
    events = []
    for page in pages:
        driver.get(page[1])
        sleep(5)
        try:
            events.extend(page[0](driver, logged_in))

        except NoSuchElementException as e:
            print("Error parsing {}".format(page[1]))
            print("No events found.")
            print(e)

        except Exception as e:
            print("Error parsing {}".format(page[1]))
            print(e)

    return events