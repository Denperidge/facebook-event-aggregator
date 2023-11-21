# Built-in imports
from sys import argv, executable
from os import makedirs, getenv, execv, getcwd
from os.path import realpath, join, abspath, dirname
from pathlib import Path
from json import dump, load
from argparse import ArgumentParser

# Local imports
from .repo import clone_or_pull_repo, update_repo
from .Event import load_events_from_json, events_to_json
from .export import events_to_html, events_to_ics, cleanup_images

from .scraper import setup_driver, scrape_all


argparse = ArgumentParser()
argparse.add_argument("--target", "-t", nargs="+", help="Facebook page to extract from. Usage: --target https://www.facebook.com/trixonline/ --target https://www.facebook.com/botaniquebxl/")
argparse.add_argument("--update", "-u", action="store_true", help="Whether to push to Git")
argparse.add_argument("--scrape", "-s", action="store_true", help="Whether to run scraper (alternatively, load from cache)")

argparse.add_argument("--host-domain", "-hd", required=True, help="Domain where your files will be hosted. E.g. https://example.com")
argparse.add_argument("--timezone", "-tz", default="Europe/London", help="What timezone to use for ics events")
argparse.add_argument("--title", default="Title", help="What title to use for the html export")

argparse.add_argument("--repo", "--repo-url", required=True, help="Domain where your files will be hosted. E.g. https://example.com")

argparse.add_argument("--remote-debugging-port", "-rdp", default=0, help="(Troubleshooting) Set Chrome debugging port. Default value: 0")


if __name__ == "__main__":
    args = argparse.parse_args()
    print(args)

    cwd = Path.cwd()
    export_dir = cwd.joinpath("public/")
    events_json_path = export_dir.joinpath("events.json") 
    img_dir = export_dir.joinpath("img/")
    


    #events_json = join(public_dir, "events.json")

    # Load .env file and startup params
    #startup_args = [arg.lower() for arg in argv[1:]]
    #headless = "headless" in startup_args
    #update = "update" in startup_args
    #scrape = "noscrape" not in startup_args
    scrape = args.scrape
    headless = True

    
    # Clone repo into public/
    clone_or_pull_repo(parent_dir_path=str(cwd), clone_dirname="public", repo_url=args.repo)
    makedirs(str(img_dir), exist_ok=True)

    if scrape:
        # Prepare img_dir in case it's needed

        # Setup Selenium scraper
        driver = setup_driver(headless, args.remote_debugging_port)

        # Scrape events
        events = scrape_all(driver, args.target, str(img_dir))
    else:
        events = load_events_from_json(events_json_path)
                

    
    # Export
    if scrape:
        events_to_json(events, str(events_json_path))

    events_to_ics(events, str(export_dir))
    events_to_html(
        events=events,
        output_dir=str(export_dir),
        absolute_img_dir=str(img_dir),
        relative_from_html_img_dir="public/",
        host_domain=args.host_domain,
        page_urls=args.target,
        timezone=args.timezone,
        title=args.title)
    cleanup_images(events, str(img_dir))

    if args.update:
        update_repo(parent_dir_path=str(cwd), clone_dirname="public")

    # Cleanup
    if scrape:
        driver.quit()
            
