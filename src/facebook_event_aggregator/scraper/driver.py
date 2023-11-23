# Built-in imports
from platform import system, machine

# Package imports
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Setup Driver
def setup_driver(chromedriver_path: str=None, headless=False, remote_debugging_port = 0, extra_opts: list[str] = []) -> webdriver.Chrome:
    options = Options()

    if (headless):
        headless_opts = [
            "--headless",
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            #"--disable-extensions",
            #"--no-sandbox",
            #"--disable-dev-shm-usage",
            #"--remote-debugging-port=" + str(remote_debugging_port),
            #"--disable-setuid-sandbox"
        ]
        for opt in headless_opts:
            options.add_argument(opt)
            #print(opt)
        for opt in extra_opts:
            options.add_argument("--" + opt)
    
    # Much thanks to https://stackoverflow.com/a/71042821
    try:
        if not chromedriver_path:
            service = Service(GeckoDriverManager().install())
        else:
            #display = Display(visible=0, size=(1920,1200))
            #display.start()
            service = Service(chromedriver_path)
            #options.binary_location = raspbian_chromium
    except:
        # Attempt selenium fallback
        service = Service()
                

    return webdriver.Firefox(service=service, options=options)


