""" IMPORTS """
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
        print(event.text)
        print()


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
        
