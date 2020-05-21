import requests
import logging
from footballapi.models import Fixture, Prediction

logging.basicConfig(level=logging.DEBUG)


class FootballApiClient:
    base_url = "https://api-football-v1.p.rapidapi.com/v2"
    status = "/status"
    predictions_prefix = "/predictions/"

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "0c7b1c5c4amshb9847dfc85a70b2p120329jsnd344652497b1"
    }

    def __init__(self):
        self.calls_counter = 0

    def get_fixtures_by_date(self, date):
        response = requests.request("GET",
                                    "https://api-football-v1.p.rapidapi.com/v2/fixtures/date/" + date,
                                    headers=self.headers)

        return self.__parse_fixtures_list(response)

    def get_prediction_for_fixture(self, fixture):
        response = requests.request("GET",
                                    self.base_url + self.predictions_prefix + fixture.fixture_id,
                                    headers=self.headers)
        logging.info("Predictions response: ")
        logging.info(response.json())
        return Prediction(response.json())

    def __parse_fixtures_list(self, response):
        result = []
        
        logging.debug("GET fixtures status: " + str(response.status_code))
        logging.debug("GET fixtures body  : " + response.json())
        fixtures_datas = response.json().get("api").get("fixtures")
        for data in fixtures_datas:
            result.append(Fixture(data))
        logging.info("found fixtures : " + str(len(result)))
        return result

    def __increase_calls_counter(self):
        self.calls_counter += 1
        logging.info(f"Logging counter + 1, current count = {self.calls_counter}")


def filter_relevant_matches(fixture):
    return fixture.status != "Match Cancelled" and \
           fixture.status != "Match Postponed"