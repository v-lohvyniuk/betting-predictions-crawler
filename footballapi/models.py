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

    def from_json(prediction_dict):
        prediction = Prediction()
        prediction.__prediction_dict = prediction_dict
        prediction = prediction_dict.get("api").get("predictions")[0]
        prediction.advice = prediction.get("advice")
        prediction.home_team_winning_percent = prediction.get("winning_percent").get("home")
        prediction.away_team_winning_percent = prediction.get("winning_percent").get("away")
        prediction.draws_team_winning_percent = prediction.get("winning_percent").get("draws")
        prediction.home_team_name = prediction.get("teams").get("home").get("team_name")
        prediction.away_team_name = prediction.get("teams").get("away").get("team_name")
        return prediction

    def __init(self):
        pass

    def __str__(self):
        string = f"{self.home_team_name} - {self.away_team_name}\n" \
               f"[{self.home_team_winning_percent}] [{self.draws_team_winning_percent}] [{self.away_team_winning_percent}]\n" \
               f"Advice: [{self.advice}]"
        if self.has_single_winner():
            return string + "\n❗ ❗ ❗ ❗ ❗ ❗ ❗ "
        return string

    @staticmethod
    def default_for_no_prediction(team1, team2):
        return team1 + " - " + team2 + " - "

    def has_single_winner(self):
        return "winner" in self.advice.lower()
