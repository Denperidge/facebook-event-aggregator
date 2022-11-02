# Package imports
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Setup Driver
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

    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)


