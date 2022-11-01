from os import getenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Driver   
# 
def setup_driver(headless=False):
    options = Options()

    if (headless):
        headless_opts = [
            "--headless",
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions"
        ]
        for opt in headless_opts:
            options.add_argument(opt)

    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


