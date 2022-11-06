# Built-in imports
from sys import argv
from os import makedirs
from os.path import realpath, join, abspath, dirname
from json import dump, load

# Package imports
from dotenv import load_dotenv

# Local imports
from repo import clone_repo_if_not_exists, update_repo
from Event import load_events_from_json, events_to_json
from scrape_and_parse.scrape_and_parse import read_pages_from_env, scrape_events
from scrape_and_parse.driver import setup_driver
from scrape_and_parse.fb_login import handle_fb_login
from export.to_ics import events_to_ics
from export.to_html import events_to_html, cleanup_images


if __name__ == "__main__":
    """ SETUP """
    # Define absolute path variables
    root_dir = abspath(join(realpath(dirname(__file__)), "../"))
    env_file = join(root_dir, ".env")

    public_dirname = "public/"
    public_dir = join(root_dir, public_dirname)

    img_dirname = "img/"
    img_dir_relative = join(public_dirname, img_dirname)
    img_dir = join(public_dir, "img/")

    events_json = join(public_dir, "events.json")

    # Load .env file and startup params
    startup_args = [arg.lower() for arg in argv[1:]]
    headless = "headless" in startup_args
    update = "update" in startup_args
    scrape = "noscrape" not in startup_args

    load_dotenv(env_file)
    pages = read_pages_from_env()

    
    # Clone repo into public/
    clone_repo_if_not_exists(parent_dir=root_dir, dest_dirname=public_dirname)

    if scrape:
        # Prepare img_dir in case it's needed
        makedirs(img_dir, exist_ok=True)

        # Setup Selenium scraper
        driver = setup_driver(headless)
        logged_in = handle_fb_login(driver, headless)

        # Scrape events
        events = scrape_events(driver, pages, logged_in, img_dir)
    else:
        events = load_events_from_json(events_json)
                

    
    # Export
    if scrape:
        events_to_json(events, events_json)
    events_to_ics(events, public_dir)
    events_to_html(events, public_dir, img_dir_relative)
    cleanup_images(events, img_dir)

    if update:
        update_repo(public_dir)


    # Cleanup
    if scrape:
        driver.quit()
            
