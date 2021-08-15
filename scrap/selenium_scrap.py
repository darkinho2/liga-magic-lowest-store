from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver(headless=False):
    options = Options()
    options.headless = headless
    options.add_argument('--no-sandbox')
    options.add_argument('--lang=es')
    options.add_argument('--disable-setuid-sandbox')
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    options.to_capabilities()
    chromedriver_path = "chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_path, options=options)
    return driver

def get_haveibeenpwned(driver):
    pass

if __name__ == '__main__':
    driver = get_driver()
