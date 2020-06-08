from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import os
import time

class DriverFactory:

    @staticmethod
    def create_new_driver():
        ChromeDriverManager().install()
        opts = Options()
        # opts.headless=True
        USER_PROFILE_DIR = os.path.dirname(os.path.abspath(__file__)) + os.sep + "chrome_profile/google-chrome"
        USER_PROFILE_DIR = USER_PROFILE_DIR.replace("\\", "/")

        opts.add_argument('--user-data-dir={}'.format(USER_PROFILE_DIR))
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        # dr
        driver = Chrome(ChromeDriverManager().install(), options=opts)
        driver.implicitly_wait(30)
        driver.set_window_size(1120, 550)
        return driver


class DriverManager:

    driver = None

    @staticmethod
    def get_driver():
        if DriverManager.driver:
            return DriverManager.driver
        else:
            DriverManager.driver = DriverFactory.create_new_driver()
            return DriverManager.driver

    @staticmethod
    def actions():
        actions = ActionChains(DriverManager.get_driver())
        return actions

    @staticmethod
    def finalize_driver():
        if DriverManager.driver:
            DriverManager.driver.quit()
            DriverManager.driver = None