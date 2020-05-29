from selenium.webdriver import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

class DriverFactory:

    @staticmethod
    def create_new_driver():
        ChromeDriverManager().install()
        opts = Options()
        ua = UserAgent()
        agent = ua.random
        opts.headless=True
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument(f'user-agent={agent}')
        # dr
        driver = Chrome(options=opts)
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
