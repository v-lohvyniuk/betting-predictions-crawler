class FixtureFilter:

    @staticmethod
    def filter_by_team_name(fixtures, name):
        results = []
        name_upper = name.upper()

        for fixture in fixtures:
            home_team = fixture.home_team_name.upper()
            away_team = fixture.away_team_name.upper()

            if name_upper in home_team or\
                    name_upper in away_team or\
                    home_team in name_upper or\
                    away_team in name_upper:
                results.append(fixture)

        return results

    @staticmethod
    def filter_by_team_names(fixtures, name1, name2):
        result_list = []
        fixtures_by_first_team = FixtureFilter.filter_by_team_name(fixtures, name1)
        fixtures_by_second_teams = FixtureFilter.filter_by_team_name(fixtures, name2)

        result_list.extend(fixtures_by_first_team)
        result_list.extend(fixtures_by_second_teams)
        return result_list
