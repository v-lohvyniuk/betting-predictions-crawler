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
                "(.//*[@class='main-markets-group '])[1]//*[@class='outcome__coeff ']")
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


    def get_top_football_events_with_small_coeff(self):
        top_events = self.try_get_top_football_events()
        events_with_coeff = list(filter(lambda x: '-' not in x.team1_win_coeff, top_events))
        return list(filter(lambda x: PariMatchCrawler.__coeff_differs_7_times(x.team1_win_coeff, x.team2_win_coeff), events_with_coeff))

    @staticmethod
    def __coeff_differs_7_times(coeff1, coeff2):
        multiplicator = 9
        return float(coeff1) / float(coeff2) >= multiplicator\
               or float(coeff2) / float(coeff1) >= multiplicator