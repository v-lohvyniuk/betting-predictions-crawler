from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:

    @staticmethod
    def create_new_driver():
        ChromeDriverManager().install()
        opts = Options()
        opts.headless=True
        driver = Chrome(options=opts)
        driver.implicitly_wait(30)
        driver.maximize_window()
        return driver


class DriverManager:

    driver = None

    @staticmethod
    def get_driver():
        if DriverManager.driver:
            return DriverManager.driver
        else:
            driver = DriverFactory.create_new_driver()
            return driver

    @staticmethod
    def finalize_driver():
        if DriverManager.driver:
            DriverManager.driver.quit()
            DriverManager.driver = None

