class Fixture:
    def __init__(self, fixture_dict):
        self.__fixtures_dict = fixture_dict
        self.home_team_name = fixture_dict.get("homeTeam").get("team_name")
        self.away_team_name = fixture_dict.get("awayTeam").get("team_name")
        self.status = fixture_dict.get("status")
        self.fixture_id = str(fixture_dict.get("fixture_id"))

    def __str__(self):
        print(self.__fixtures_dict)


class Prediction:

    def __init__(self, prediction_dict):
        self.__prediction_dict = prediction_dict
        self.advice = prediction_dict.get("api").get("predictions")[0].get("advice")
        self.home_team_winning_percent = prediction_dict.get("api").get("predictions")[0].get("winning_percent").get("home")
        self.away_team_winning_percent = prediction_dict.get("api").get("predictions")[0].get("winning_percent").get("away")
        self.draws_team_winning_percent = prediction_dict.get("api").get("predictions")[0].get("winning_percent").get("draws")
        self.home_team_name = prediction_dict.get("api").get("predictions")[0].get("teams").get("home").get("team_name")
        self.away_team_name = prediction_dict.get("api").get("predictions")[0].get("teams").get("away").get("team_name")

    def __init(self):
        pass

    def __str__(self):
        return \
f"""{self.home_team_name} - {self.away_team_name} [{self.home_team_winning_percent}] [{self.draws_team_winning_percent}] [{self.away_team_winning_percent}] Advice: [{self.advice}]"""

    @staticmethod
    def default_for_no_prediction(team1, team2):
        return team1 + " " + team2 + " - No predictions"
