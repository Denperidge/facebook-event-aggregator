""" IMPORTS """
from scrape_and_parse.scrape_and_parse import read_pages_from_env, scrape_events
from scrape_and_parse.driver import setup_driver
from scrape_and_parse.fb_login import handle_fb_login

from dotenv import load_dotenv
from json import dump
from os import makedirs
from os.path import realpath, join, abspath, dirname
from sys import argv
from repo import init_repo_if_not_exists



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
    try:
        if (argv[1] == "headless"):
            headless = True
    except IndexError:
        pass
    page_load_time = 5
    pages = read_pages_from_env()

    
    # Create public/ repo
    makedirs(public_dir, exist_ok=True)
    init_repo_if_not_exists(public_dir)

    # Setup Selenium scraper
    driver = setup_driver(headless)
    logged_in = handle_fb_login(driver, headless)

    # Scrape events
    events = scrape_events(driver, pages, logged_in)
    

    """ CLEANUP """
    with open(events_json, "w") as file:
        dump(events, file)
    driver.quit()
            
