# utils/driver_factory.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config_reader import read_config

def get_driver():
    cfg = read_config()  # reads the [DEFAULT] section from config/config.ini

    browser = cfg.get("browser", "chrome").lower()
    headless = cfg.getboolean("headless", False)
    implicit_wait = cfg.getint("implicit_wait", 10)

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(implicit_wait)
    return driver
