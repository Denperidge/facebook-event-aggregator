from .regex import find_and_remove, re_line_with_characters, re_guests, re_three_letter_two_digit_date, re_utc_time
from Event import Event
from selenium.webdriver.common.by import By
from time import sleep

""" PARSING FUNCTIONS """
def parse_page(driver, logged_in):
    event_container = driver.find_element(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]""")
    events = event_container.find_elements(By.XPATH, "*")
    for event in events:
        print("Detected upcoming event in {}!".format("page"))
        print(event.text)
        print()

def parse_community(driver, logged_in):
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


def handle_fb_login(driver, email, password):
    driver.get("https://www.facebook.com/login")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    sleep(5)