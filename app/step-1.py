""" IMPORTS """
from datetime import date
from operator import truediv
from pprint import pprint
from scrape_and_parse.driver import setup_driver
from selenium.common.exceptions import NoSuchElementException

from time import sleep
from dotenv import load_dotenv
from json import loads, dump
from os import getenv, makedirs
from os.path import realpath, join, abspath, dirname
from sys import argv
from getpass import getpass
from repo import init_repo_if_not_exists



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

    headless = False
    if (argv[1] == "headless"):
        headless = True
    driver = setup_driver(headless)
 
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
            
