class MatchRowDTO:
    def __init__(self, team_1, team_2, time_str, team1_win_coeff, noone_coeff, team2_win_coeff):
        self.team1 = team_1
        self.team2 = team_2
        self.time_str = time_str
        self.team1_win_coeff = team1_win_coeff
        self.team2_win_coeff = team2_win_coeff
        self.noone_coeff = noone_coeff

    def __str__(self) -> str:
        return f"{self.team1} {self.team2} {self.time_str} {self.team1_win_coeff} {self.noone_coeff} {self.team2_win_coeff}"


