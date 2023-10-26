from time import sleep

from .driver import setup_driver
from ..utils.url_converter import facebook_www_to_locale

from selenium.webdriver.common.by import By

from os import getenv
from os.path import join, realpath
from time import sleep
from json import loads
from urllib.request import urlretrieve

# Package imports
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Local imports
from ..utils.fb_regexes import find_and_remove, regex_in, re_line_with_characters, re_guests, re_three_letter_two_digit_date, re_utc_time, re_utc_and_more
from ..Event import Event
from .driver import setup_driver
from ..utils.url_converter import facebook_www_to_locale

from .utils import save_image
from .scrape_event_page import scrape_event_page

from time import sleep

def scrape_events_page(driver, event_url, img_dir) -> list[Event]:
    driver.get(event_url)
    sleep(20)
    source = driver.find_element(By.XPATH, "//h1").text.strip()
    event_container = driver.find_element(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]""")
    raw_events = event_container.find_elements(By.XPATH, "*")
    events = []
    for event in raw_events:
        print("Detected upcoming event in {}!".format("page"))
        raw_data = event.text
        if regex_in(raw_data, re_utc_and_more): # Events with multiple times have multiple entries + one main. This is the main, so skip it
            print("detected main event with times, skipping current")
            continue

        try:
            lines = raw_data.split("\n")
            name = lines[1]
            datetime = lines[0]
            url = ""
            location = ""
        except IndexError:
            print("Failed to add event from page")
            print("Provided data: {}".format(lines))
            continue
    
        try:
            # find_element doesn't work, perhaps due to grandchild?
            urls = event.find_elements(By.TAG_NAME, "a")
            url = urls[0].get_attribute("href")
        except IndexError:
            print("No url found")
        
        location, image_url = scrape_event_page(url)

        event = Event(name, datetime, source, location, url)
        events.append(event)

        if image_url:
            save_image(event, image_url, img_dir)

        
    return events