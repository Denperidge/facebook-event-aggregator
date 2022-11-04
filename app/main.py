# Built-in imports
from sys import argv
from os import makedirs
from os.path import realpath, join, abspath, dirname
from json import dump

# Package imports
from dotenv import load_dotenv

# Local imports
from repo import clone_repo_if_not_exists, update_repo
from scrape_and_parse.scrape_and_parse import read_pages_from_env, scrape_events
from scrape_and_parse.driver import setup_driver
from scrape_and_parse.fb_login import handle_fb_login
from export.to_ics import events_to_ics


if __name__ == "__main__":
    """ SETUP """
    # Define absolute path variables
    root_dir = abspath(join(realpath(dirname(__file__)), "../"))
    env_file = join(root_dir, ".env")
    public_dirname = "public/"
    public_dir = join(root_dir, public_dirname)
    events_json = join(public_dir, "events.json")

    # Load .env file and startup params
    startup_args = [arg.lower() for arg in argv]
    headless = "headless" in startup_args
    update = "update" in startup_args

    load_dotenv(env_file)
    pages = read_pages_from_env()

    
    # Clone repo into public/
    clone_repo_if_not_exists(parent_dir=root_dir, dest_dirname=public_dirname)

    # Setup Selenium scraper
    driver = setup_driver(headless)
    logged_in = handle_fb_login(driver, headless)

    # Scrape events
    events = scrape_events(driver, pages, logged_in)
    
    # Export
    with open(events_json, "w") as file:
        dump(events, file)
    events_to_ics(events, public_dir)

    if update:
        update_repo(public_dir)


    # Cleanup
    driver.quit()
            
