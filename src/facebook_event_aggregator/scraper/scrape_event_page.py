from time import sleep

from .driver import setup_driver
from ..utils.url_converter import facebook_www_to_locale

from selenium.webdriver.common.by import By

# Parse the event page in a secondary driver. This is universal for pages & communities
def scrape_event_page(event_url):
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
        image_url = tmp_driver.find_element(By.CSS_SELECTOR,'img[data-imgperflogname="profileCoverPhoto"]').get_attribute("src")

        sleep(5)

        tmp_driver.quit()
                
    except Exception as e:
        print(e)
        print("Location could not be fetched")

    
    return location, image_url
