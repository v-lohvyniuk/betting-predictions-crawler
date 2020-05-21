from crawler.driver import DriverManager
from crawler.models import MatchRowDTO
import logging

logging.basicConfig(level=logging.DEBUG)


class PariMatchCrawler:
    def __init__(self):
        self.driver = DriverManager.get_driver()
        self.driver.get("https://air2.pm-511.info/en/")

    def get_top_football_events(self):
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


# class PariMatchScrapperCrawler:
#     def __init__(self):
#         self.page = requests.get('https://en.parimatch.com/en/')
#         self.tree = html.fromstring(self.page.content)
#
#     def get_cards_content(self):
#         return self.tree.xpath("//*[@data-id='top-widget-carousel-soccer']//*[@data-id='event-card']")
#
#     def __get_card_xpath_by_position(self, pos):
#         specific_football_card_xpath = "(//*[@data-id='top-widget-carousel-soccer']//*[@data-id='event-card'])[{}]"
#         return specific_football_card_xpath.format(pos)
#
#     def __get_card_time_xpath_by_position(self, pos):
#         specific_football_card_time_xpath = "(//*[@data-id='top-widget-carousel-soccer']//*[@data-id='event-card-time-status-text-prematch'])[{}]"
#         return specific_football_card_time_xpath.format(pos)
#
#     def get_top_football_events(self):
#
#         dto_list = []
#         for card_pos in range(1, len(self.get_cards_content()) + 1):
#             first_team_xpath = "(" + self.__get_card_xpath_by_position(card_pos) + "//" + "span" + ")" + "[1]"
#             secnd_team_xpath = "(" + self.__get_card_xpath_by_position(card_pos) + "//" + "span" + ")" + "[2]"
#             first_twin_xpath = "(" + self.__get_card_xpath_by_position(card_pos) + "//" + "span" + ")" + "[3]"
#             draws_twin_xpath = "(" + self.__get_card_xpath_by_position(card_pos) + "//" + "span" + ")" + "[4]"
#             secnd_twin_xpath = "(" + self.__get_card_xpath_by_position(card_pos) + "//" + "span" + ")" + "[5]"
#             datetime_xpath = self.__get_card_time_xpath_by_position(card_pos)
#
#             team_1 = self.tree.xpath(first_team_xpath)
#             team_2 = self.tree.xpath(secnd_team_xpath)
#             team_1_win_coeff = self.tree.xpath(first_twin_xpath)
#             noone_coeff = self.tree.xpath(draws_twin_xpath)
#             team_2_win_coeff = self.tree.xpath(secnd_twin_xpath)
#             time = self.tree.xpath(datetime_xpath)
#
#             dto_list.append(MatchRowDTO(team_1, team_2, time, team_1_win_coeff, noone_coeff, team_2_win_coeff))
#
#         return dto_list
