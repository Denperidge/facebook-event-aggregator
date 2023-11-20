# Built-in imports
from platform import system, machine

# Package imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Driver
def setup_driver(headless=False, is_linux_armv7l=(system() == "Linux" and machine() == "armv7l")) -> webdriver.Chrome:
    options = Options()

    if (headless):
        headless_opts = [
            "--headless=new",
            "--disable-gpu",
            "--window-size=1920,1200",
            #"---ignore-certificate-errors",
            #"--disable-extensions",
            #"--no-sandbox",
            #"--disable-dev-shm-usage",
            "--remote-debugging-port=9223",
            #"--disable-setuid-sandbox"
        ]
        for opt in headless_opts:
            options.add_argument(opt)
            #print(opt)
    
    # Much thanks to https://stackoverflow.com/a/71042821
    try:
        if not is_linux_armv7l:
            service = Service(ChromeDriverManager().install())
        else:
            #display = Display(visible=0, size=(1920,1200))
            #display.start()
            raspbian_chromium = "/usr/lib/chromium-browser/chromedriver"
            service = Service(raspbian_chromium)
            #options.binary_location = raspbian_chromium
    except:
        # Attempt selenium fallback
        service = Service()
                

    return webdriver.Chrome(service=service, options=options)


