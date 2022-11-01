from .regex import find_and_remove, re_line_with_characters, re_guests, re_three_letter_two_digit_date, re_utc_time
from Event import Event
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from time import sleep
from json import loads
from os import getenv

""" PARSING FUNCTIONS """
def parse_page(driver, logged_in):
    event_container = driver.find_element(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]""")
    events = event_container.find_elements(By.XPATH, "*")
    for event in events:
        print("Detected upcoming event in {}!".format("page"))
        print(event.text)
        print()

def parse_community(driver, logged_in):
    print(driver.find_element(By.TAG_NAME,"body").text)
    
    if not logged_in:
        event_container = driver.find_element(By.ID, "upcoming_events_card").find_element(By.TAG_NAME, "table")
        events = event_container.find_elements(By.TAG_NAME, "tr")
    else:
        events = driver.find_elements(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div/div/*""")
        events.pop(0)  # First element is title

    for event in events:
        print("Detected upcoming event in {}!".format("community"))
        raw_data = event.text

        (raw_data, date) = find_and_remove(raw_data, re_three_letter_two_digit_date)
        (raw_data, time) = find_and_remove(raw_data, re_utc_time)
        (raw_data, guests) = find_and_remove(raw_data, re_guests)  # Unused
        (raw_data, name) = find_and_remove(raw_data, re_line_with_characters)

        datetime = date + " " + time
        location = raw_data.replace("\n", " ").strip()

        event = Event(name, datetime, location)

        print(event.location)

        return event


def read_pages_from_env():
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
        
        pages.append((func, url))
    return pages


def scrape_events(driver, pages, logged_in):
    """ RUNNING PARSE FUNCTIONS ON PAGES """
    events = []
    for page in pages:
        driver.get(page[1])
        sleep(5)
        try:
            events.append(page[0](logged_in).__dict__)  # __dict__ is to allow json dump

        except NoSuchElementException:
            print("No events found for " + page[1])

        except Exception as e:
            print("Error")
            print(e)