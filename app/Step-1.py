""" IMPORTS """
from datetime import date
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
from json import loads
from os import getenv
from os.path import realpath, join, abspath, dirname
from dateutil import parser
import re


""" REGEX """
# These are for parsing the scraping.


"""
Example:
    NOV
    11
    Text

    Returns: 
        Nov
        11
"""
re_three_letter_two_digit_date = r"^[a-zA-Z]{3}\W\d{1,2}$"

"""
Example:
    Fri 19:00 UTC+01 · 84 guests

    returns: Fri 19:00 UTC+01
"""
re_utc_time = r".*UTC\+\d{2}"

"""
Example:
    NOV
    19
    Name - 32 guests

    Returns: Name - 32 guests 
"""
re_guests = r".*guest.*"

# Matches any line with 1 or more characters
re_line_with_characters = r"^.{1,}$"



def find_and_remove(data, pattern):
    found = re.search(pattern, data, flags=re.MULTILINE).group()
    data = data.replace(found, "")
    return data, found


""" CLASS """
class Event:
    """
    name = str
    datetime = date
    url = str
    """


    def __init__(self, name, datetime, location, url=""):
        self.name = name
        self.datetime = parser.parse(datetime)
        self.location = location
        self.url = url


""" SETUP """
# Load .env, install & set Selenium driver
app_dir = realpath(dirname(__file__))
env_file = abspath(join(app_dir, "../", ".env"))
load_dotenv(env_file)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

""" PARSING FUNCTIONS """
def parse_page():
    event_container = driver.find_element(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]""")
    events = event_container.find_elements(By.XPATH, "*")
    for event in events:
        print("Detected upcoming event in {}!".format("page"))
        print(event.text)
        print()

def parse_community():
    event_container = driver.find_element(By.ID, "upcoming_events_card").find_element(By.TAG_NAME, "table")
    events = event_container.find_elements(By.TAG_NAME, "tr")
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



        print(event)


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
        

""" RUNNING PARSE FUNCTIONS ON PAGES """
for page in pages:
    driver.get(page[1])
    sleep(5)
    try:
        page[0]()

    except NoSuchElementException:
        print("No events found for " + page[1])

    except Exception as e:
        print("Error")
        pprint(e)

""" CLEANUP """
driver.quit()
        
