from crawler.driver import DriverManager
from crawler.models import MatchRowDTO
import logging
import datetime
logging.basicConfig(level=logging.INFO)
import calendar
import time


class PariMatchCrawler:

    def __init__(self):
        self.driver = DriverManager.get_driver()

    def is_logged_in(self):
        return "BALANCE" in self.driver.page_source

    def __populate_cookies(self):
        cookies = self.driver.get_cookies()
        self.driver.delete_all_cookies()
        self.driver.refresh()
        for cookie in cookies:
            if 'expiry' in cookie.keys():
                future = datetime.datetime.utcnow() + datetime.timedelta(days=700)
                cookie['expiry'] = calendar.timegm(future.timetuple())
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def open_home_page(self):
        self.driver.get("https://air2.parimatch.com/en/")
        time.sleep(5)
        # self.__populate_cookies()

    def login_if_needed(self):
        try:
            self.driver.find_element_by_xpath("//*[contains(@class, 'btn-login')]").click()
            self.driver.find_element_by_id("login").send_keys("volodymyr.lohvyniuk@gmail.com")
            self.driver.find_element_by_id("password").send_keys("Vovazjambo18")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Exception was happen: {e}")

    def get_top_football_events(self):
        self.driver = DriverManager.get_driver()
        self.driver.get("https://air2.pm-511.info/en/")
        self.actions = DriverManager.actions()

        football_tab = self.driver.find_element_by_xpath(
            "//*[contains(@class, 'tab__title') and contains(text(), 'Football')]")
        football_tab.click()

        events_table = self.driver.find_element_by_id("sport-id")

        event_rows = events_table.find_elements_by_class_name("top-event__wrapper")

        dto_list = []

        for row in event_rows:
            time = row.find_element_by_class_name("top-event-date").text
            team_elements = row.find_elements_by_css_selector(".top-event__competitor")
            team_1 = team_elements[0].text
            team_2 = team_elements[1].text
            coeffs_els = row.find_elements_by_xpath(
                "(//*[@class='main-markets-group '])[1]//*[@class='outcome__coeff ']")
            team_1_win_coeff = coeffs_els[0].text
            noone_coeff = coeffs_els[1].text
            team_2_win_coeff = coeffs_els[2].text

            dto_list.append(MatchRowDTO(team_1, team_2, time, team_1_win_coeff, noone_coeff, team_2_win_coeff))
        logging.info("Selenium PariMatchCrawler finished execution")
        DriverManager.finalize_driver()
        return dto_list

    def try_get_top_football_events(self):
        try:
            return self.get_top_football_events()
        except Exception:
            logging.error("Can't fetch all top football predictions")
        return []


bot = PariMatchCrawler()
bot.open_home_page()
bot.login_if_needed()
bot.is_logged_in()
