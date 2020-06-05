from crawler.crawlers import PariMatchCrawler
from crawler.models import MatchRowDTO
from footballapi.client import FootballApiClient
from footballapi.models import Prediction
from footballapi.filters import FixtureFilter
from datetime import datetime
from db.dao import EventDao
import logging

logging.basicConfig(level=logging.INFO)

from time import strptime


class PredictionIntegrationService:

    def __init__(self):
        self.crawler = PariMatchCrawler()
        self.apiclient = FootballApiClient()
        self.fixtures_by_date_cash = {}

    def get_predictions_for_new_matches(self):
        events_list = self.crawler.try_get_top_football_events()
        event_dao = EventDao()
        new_events_list = list(filter(lambda x: not event_dao.event_for_teams_present(x.team1, x.team2), events_list))
        predictions = []
        for event in new_events_list:
            try:
                prediction = self.get_match_prediction(event)
                if type(prediction) is not str:
                    predictions.append(prediction)
            except Exception as e:
                logging.info("Error during fetching prediction for event: {}\n{}".format(event, e))
        EventDao().put_if_not_present(predictions)
        return predictions

    def get_predictions_for_new_matches_with_single_winner(self):
        all_new = self.get_predictions_for_new_matches()
        winners_only = list(filter(lambda x: x.has_single_winner(), all_new))
        return winners_only

    def  get_predictions_for_all_matches(self):
        events_list = self.crawler.try_get_top_football_events()
        predictions = []
        for event in events_list:
            try:
                prediction = self.get_match_prediction(event)
                if type(prediction) is not str:
                    predictions.append(prediction)
            except Exception as e:
                logging.info("Error during fetching prediction for event: {}\n{}".format(event, e))
        return predictions

    def get_predictions_with_single_winner(self):
        predictions = self.get_predictions_for_all_matches()
        filtered = list(filter(lambda x: x.has_single_winner(), predictions))
        return filtered

    def get_match_prediction(self, event: MatchRowDTO):
        event_date = PredictionIntegrationService.__format_event_date(event.time_str)

        fixtures = self.get_fixtures_from_cache(event_date)
        fixtures = FixtureFilter.filter_by_team_names(fixtures, event.team1, event.team2)
        if len(fixtures) == 0:
            return Prediction.default_for_no_prediction(event.team1, event.team2)
        else:
            prediction = self.apiclient.get_prediction_for_fixture(fixtures[0])

        return prediction

    def get_fixtures_from_cache(self, datetime):
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

        event_date = f"{str(datetime.now().year)}-{month_number}-{month_day}"
        return event_date

