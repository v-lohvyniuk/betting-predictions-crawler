from crawler.driver import DriverManager
from crawler.models import MatchRowDTO
import logging

logging.basicConfig(level=logging.INFO)


class PariMatchCrawler:

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