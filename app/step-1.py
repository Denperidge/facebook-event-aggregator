""" IMPORTS """
from datetime import date
from operator import truediv
from pprint import pprint
from scrape_and_parse.driver import setup_driver
from scrape_and_parse.fb_login import handle_fb_login
from selenium.common.exceptions import NoSuchElementException

from scrape_and_parse.scrape_and_parse import parse_page, parse_community
from time import sleep
from dotenv import load_dotenv
from json import loads, dump
from os import getenv, makedirs
from os.path import realpath, join, abspath, dirname
from sys import argv
from repo import init_repo_if_not_exists

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


if __name__ == "__main__":
    """ SETUP """
    # Define absolute path variables
    root_dir = abspath(join(realpath(dirname(__file__)), "../"))
    env_file = join(root_dir, ".env")
    public_dir = join(root_dir, "public/")
    events_json = join(public_dir, "events.json")

    # Load .env file and startup params
    load_dotenv(env_file)
    headless = False
    if (argv[1] == "headless"):
        headless = True
    page_load_time = 5
    
    # Create public/ repo
    makedirs(public_dir, exist_ok=True)
    init_repo_if_not_exists(public_dir)

    # Setup Selenium scraper
    driver = setup_driver(headless)
    logged_in = handle_fb_login(driver, headless)

    pages = read_pages_from_env()
    

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
            
