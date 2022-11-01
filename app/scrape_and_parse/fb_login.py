# Built-in imports
from os import getenv
from time import sleep
from getpass import getpass

# Package imports
from selenium.webdriver.common.by import By

def handle_fb_login(driver, headless):
    # If an email is provided, log into Facebook
    logged_in = False
    if getenv("facebook_email") is not None:
        facebook_email = getenv("facebook_email")
        print("Facebook email passed...")
        # Password provided, use that
        if getenv("facebook_password") is not None:
            print("... and a password. Using that to login.")
            facebook_password = getenv("facebook_password")
            login(driver, facebook_email, facebook_password)
            logged_in = True

        # No password provided, but running interactively, so prompt
        elif not headless:
            print("... but no password. Please enter it in the following prompt:")
            facebook_password = getpass()
            login(driver, facebook_email, facebook_password)
            logged_in = True
        
        # No password provided, but running headless, so quit
        else:
            print("Email was passed, but no password in headless mode. Skipping login")    
    
    return logged_in

def login(driver, email, password):
    driver.get("https://www.facebook.com/login")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    sleep(5)