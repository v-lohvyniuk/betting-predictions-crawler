from crawler.crawlers import PariMatchCrawler
from crawler.models import MatchRowDTO
from footballapi.client import FootballApiClient
from footballapi.models import Prediction
from footballapi.filters import FixtureFilter
from datetime import datetime

from time import strptime


class PredictionIntegrationService:

    def __init__(self, crawler: PariMatchCrawler, apiclient:FootballApiClient):
        self.crawler = crawler
        self.apiclient = apiclient
        self.fixtures_by_date_cash = {}

    def get_matches_predictions(self):
        events_list = self.crawler.get_top_football_events()
        predictions = []
        for event in events_list:
            prediction = self.get_match_prediction(event)
            predictions.append(prediction)

        return predictions

    def get_match_prediction(self, event: MatchRowDTO):
        event_date = PredictionIntegrationService.__format_event_date(event.time_str)

        fixtures = self.get_fixtures_from_cash(event_date)
        fixtures = FixtureFilter.filter_by_team_names(fixtures, event.team1, event.team2)
        if len(fixtures) == 0:
            return Prediction.default_for_no_prediction(event.team1, event.team2)
        else:
            prediction = self.apiclient.get_prediction_for_fixture(fixtures[0])

        return prediction

    def get_fixtures_from_cash(self, datetime):
        if datetime in self.fixtures_by_date_cash:
            return self.fixtures_by_date_cash[datetime]
        fixtures_list = self.apiclient.get_fixtures_by_date(datetime)
        self.fixtures_by_date_cash[datetime] = fixtures_list
        return self.fixtures_by_date_cash[datetime]

    @staticmethod
    def __format_event_date(time_str):
        date_items = time_str.replace('\n', ' ').split(' ')
        if date_items[0] == "LIVE":
            month_number = ("0" + str(datetime.now().month))[-2:]
            month_day = datetime.now().day
        else:
            month = date_items[2]
            month_day = date_items[1]
            month_number = ("0" + str(strptime(month, '%b').tm_mon))[-2:]
        event_date = f"2020-{month_number}-{month_day}"
        return event_date

