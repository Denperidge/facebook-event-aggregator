from facebook_scraper import get_posts
from pprint import pprint
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))



def parse_page():
    event_container = driver.find_element(By.XPATH, """//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]""")
    events = event_container.find_elements(By.XPATH, "*")
    for event in events:
        print("Detected upcoming event!")
        print(event.text)
        print()

def parse_community():
    event_container = driver.find_element(By.ID, "upcoming_events_card").find_element(By.TAG_NAME, "table")
    events = event_container.find_elements(By.TAG_NAME, "tr")
    for event in events:
        print("Detected upcoming event!")
        print(event.text)
        print()


pages = [
    (parse_page, "https://www.facebook.com/ID/upcoming_hosted_events"),
    (parse_community, "https://www.facebook.com/ID/events/?ref=page_internal")
]


for page in pages:
    print(page[1])
    #soup = BeautifulSoup(get(page[1]).content, "html.parser")
    driver.get(page[1])
    sleep(5)

    try:
        page[0]()


        #print(list(soup.find("img").parents)[2])
    except Exception as e:
        print("Error")
        pprint(e)

driver.quit()
        
