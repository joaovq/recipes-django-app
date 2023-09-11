from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from time import sleep

# Path(__file__) traz o path completo desse arquivo
ROOT_PATH = Path(__file__).parent.parent
CHROME_DRIVER_NAME = 'chromedriver.exe'
CHROME_DRIVER_PATH = ROOT_PATH / 'bin' / CHROME_DRIVER_NAME

print(CHROME_DRIVER_PATH)
print(ROOT_PATH)
"""Não mostra o navegador (--headless)"""
util_options = (
    '--headless' 
)

def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    if os.environ.get('SELENIUM_HEADLESS',False) == '1':
        chrome_options.add_argument('--headless')        
    chrome_service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser        


if __name__ == '__main__':
    browser = make_chrome_browser(util_options)
    sleep(5)
    browser.get('https://www.google.com.br') 
