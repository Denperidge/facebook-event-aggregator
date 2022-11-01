""" IMPORTS """
from datetime import date
from operator import truediv
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
from json import loads, dump
from os import getenv, makedirs
from os.path import realpath, join, abspath, dirname
from dateutil import parser
from sys import argv
from getpass import getpass
import re
from repo import init_repo_if_not_exists, update_repo


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
class Event(object):
    """
    name = str
    datetime = date
    url = str
    """


    def __init__(self, name, datetime, location, url=""):
        self.name = name
        # Replacement due to bug ? https://github.com/dateutil/dateutil/issues/70#issuecomment-945080282
        self.datetime = parser.parse(datetime.replace("UTC", "")).isoformat()
        self.location = location
        self.url = url


""" PARSING FUNCTIONS """
def parse_page(logged_in):
    event_container = driver.find_element(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]""")
    events = event_container.find_elements(By.XPATH, "*")
    for event in events:
        print("Detected upcoming event in {}!".format("page"))
        print(event.text)
        print()

def parse_community(logged_in):
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


def handle_fb_login(email, password):
    driver.get("https://www.facebook.com/login")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    sleep(5)


if __name__ == "__main__":
    """ SETUP """
    # Load .env, install & set Selenium driver
    root_dir = abspath(join(realpath(dirname(__file__)), "../"))
    env_file = join(root_dir, ".env")
    public_dir = join(root_dir, "public/")

    init_repo_if_not_exists(public_dir)

    events_json = join(public_dir, "events.json")
    makedirs(public_dir, exist_ok=True)
    load_dotenv(env_file)
    page_load_time = 5
    # Much thanks to https://github.com/jsoma/selenium-github-actions
    options = Options()
    try:
        if (argv[1] == "headless"):
            headless = True
            headless_opts = [
                "--headless",
                "--disable-gpu",
                "--window-size=1920,1200",
                "--ignore-certificate-errors",
                "--disable-extensions"
            ]
            for opt in headless_opts:
                options.add_argument(opt)
            page_load_time = 10
        else:
            headless = False

    except IndexError:
        headless = False  # No arguments were passed, assume not headless

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


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
    
    # If an email is provided, log into Facebook
    logged_in = False
    if getenv("facebook_email") is not None:
        facebook_email = getenv("facebook_email")
        print("Facebook email passed...")
        # Password provided, use that
        if getenv("facebook_password") is not None:
            print("... and a password. Using that to login.")
            facebook_password = getenv("facebook_password")
            handle_fb_login(facebook_email, facebook_password)
            logged_in = True

        # No password provided, but running interactively, so prompt
        elif not headless:
            print("... but no password. Please enter it in the following prompt:")
            facebook_password = getpass()
            handle_fb_login(facebook_email, facebook_password)
            logged_in = True
        
        # No password provided, but running headless, so quit
        else:
            print("Email was passed, but no password in headless mode. Skipping login")    



    """ RUNNING PARSE FUNCTIONS ON PAGES """
    events = []
    for page in pages:
        driver.get(page[1])
        sleep(page_load_time)
        try:
            events.append(page[0](logged_in).__dict__)  # __dict__ is to allow json dump

        except NoSuchElementException:
            print("No events found for " + page[1])

        except Exception as e:
            print("Error")
            pprint(e)

    """ CLEANUP """
    with open(events_json, "w") as file:
        dump(events, file)
    driver.quit()
            
