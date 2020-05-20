from footballapi.client import FootballApiClient, Fixture
from footballapi.filters import FixtureFilter

client = FootballApiClient()
desired_date = "2020-05-16"
date = str(input("Type date in format YYYY-MM-DD (e.g. 2020-05-16) "))
fixtures_by_date = client.get_fixtures_by_date(date)

while(True):
    first_team_name = input("First team (e.g. 'borussia') ")
    second_team_name = input("Second team (e.g. 'schalke') ")

    teams_fixture = FixtureFilter.filter_by_team_names(fixtures_by_date, first_team_name, second_team_name)[0]

    prediction = client.get_prediction_for_fixture(teams_fixture)
    print(prediction)

