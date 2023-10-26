# Built-in imports
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
from Event import Event
from .driver import setup_driver
from ..utils.url_converter import facebook_www_to_locale

""" PARSING FUNCTIONS """

class ScrapeTarget():
    pass

def scrape_all(driver, pages: [], logged_in, img_dir):
    """ RUNNING PARSE FUNCTIONS ON PAGES """
    img_dir = realpath(img_dir)  # Directory where images get stored

    events = []
    for page in pages:
        driver.get(page[1])
        sleep(5)
        try:
            events.extend(page[0](driver, logged_in, img_dir))

        except NoSuchElementException as e:
            print("Error parsing {}".format(page[1]))
            print("No events found.")
            print(e)

        except Exception as e:
            print("Error parsing {}".format(page[1]))
            raise e

    return events
