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
from .regex import find_and_remove, regex_in, re_line_with_characters, re_guests, re_three_letter_two_digit_date, re_utc_time, re_utc_and_more
from Event import Event
from scrape_and_parse.driver import setup_driver
from scrape_and_parse.locale import facebook_www_to_locale

""" PARSING FUNCTIONS """
def parse_page(driver, logged_in, img_dir):
    source = driver.find_element(By.XPATH, "//h1").text
    event_container = driver.find_element(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]""")
    raw_events = event_container.find_elements(By.XPATH, "*")
    events = []
    for event in raw_events:
        print("Detected upcoming event in {}!".format("page"))
        raw_data = event.text
        if regex_in(raw_data, re_utc_and_more): # Events with multiple times have multiple entries + one main. This is the main, so skip it
            print("detected main event with times, skipping current")
            continue

        try:
            lines = raw_data.split("\n")
            name = lines[1]
            datetime = lines[0]
            url = ""
            location = ""
        except IndexError:
            print("Failed to add event from page")
            print("Provided data: {}".format(lines))
            continue
    
        try:
            # find_element doesn't work, perhaps due to grandchild?
            urls = event.find_elements(By.TAG_NAME, "a")
            url = urls[0].get_attribute("href")
        except IndexError:
            print("No url found")
        
        location, image_url = parse_event(url)

        event = Event(name, datetime, source, location, url)
        events.append(event)

        if image_url:
            save_image(event, image_url, img_dir)

        
    return events

def parse_community(driver, logged_in, img_dir):
    #print(driver.find_element(By.TAG_NAME,"body").text)
    source = driver.find_element(By.XPATH, "//h1").text
    
    if not logged_in:
        event_container = driver.find_element(By.ID, "upcoming_events_card").find_element(By.TAG_NAME, "table")
        raw_events = event_container.find_elements(By.TAG_NAME, "tr")
    else:
        raw_events = driver.find_elements(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div/div/*""")
        raw_events.pop(0)  # First element is title

    events = []
    for event in raw_events:
        print("Detected upcoming event in {}!".format("community"))
        raw_data = event.text


        (raw_data, date) = find_and_remove(raw_data, re_three_letter_two_digit_date)
        (raw_data, time) = find_and_remove(raw_data, re_utc_time)
        (raw_data, guests) = find_and_remove(raw_data, re_guests)  # Unused
        (raw_data, name) = find_and_remove(raw_data, re_line_with_characters)
        url = event.find_element(By.TAG_NAME, "a").get_attribute("href")

        datetime = date + " " + time
        
        try:
            location = event.find_elements(By.TAG_NAME, "td")[2].text.replace("\n", " ")
        except NoSuchElementException:
            print("Location could not be fetched")

        event = Event(name, datetime, source, location, url)

        events.append(event)

        try:
            (location, image_url) = parse_event(url)
            if image_url:
                save_image(event, image_url, img_dir)
        except Exception as e:
            print(e)
    return events

# Parse the event page in a secondary driver. This is universal for pages & communities
def parse_event(event_url):
    location = None
    image_url = None
    event_url = facebook_www_to_locale(event_url)
    try:
        print("Searching for location & image in " + event_url)
        tmp_driver = setup_driver(headless=True)
        tmp_driver.get(event_url)
        sleep(20)
        info_rows = tmp_driver.find_elements(By.XPATH, "//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div/*")
        # Assume the first row is location, except if it contains specific text
        for info_row in info_rows:
            info = info_row.text
            info_lower = info.lower()
            if "details" in info_lower or "event by" in info_lower or "people respon" in info_lower:
                continue
                    
            # If location hasn't been found yet, assume the first line (that isn't excluded) is
            location = info
            break
            """ The following code can be used to begin implementing duration
            if not location:
                location = info
            if "duration" in info_lower:
                pass  
            """
                
        image_url = tmp_driver.find_element(By.CSS_SELECTOR,"img[data-imgperflogname=\"profileCoverPhoto\"]").get_attribute("src")

        tmp_driver.quit()
                
    except Exception as e:
        print(e)
        print("Location could not be fetched")

    
    return (location, image_url)

def read_pages_from_env(replace_locale=True):
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
    
        if replace_locale:
            # Specify localisation
            url = facebook_www_to_locale(url)

        pages.append((func, url))
    return pages


def save_image(event, image_url, img_dir):
    if ".png" in image_url:
        ext = ".png"
    else:
        ext = ".jpg"
    print(event.uid)
    urlretrieve(image_url, join(img_dir, event.uid + ext))


def scrape_events(driver, pages, logged_in, img_dir):
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
