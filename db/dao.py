from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.ext.declarative import declarative_base
from footballapi.models import Prediction
from crawler.models import MatchRowDTO

Base = declarative_base()

user = "ndsqqccomgcjru"
password = "7731f0b85d92b20adabadde4bfdcf2f2527534119324422e631bd5ef4f5dabdf"
host = "ec2-46-137-84-140.eu-west-1.compute.amazonaws.com"
port = "5432"
database = "d6acmb8v2cqk01"

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    team1 = Column(String)
    team2 = Column(String)
    event_date = Column(String)
    first_team_cof = Column(String)
    draws_cof = Column(String)
    second_team_cof = Column(String)
    advice = Column(String)
    sent_to_user = Column(Boolean)

    @staticmethod
    def from_prediction(prediction: Prediction):
        return Event(team1=prediction.home_team_name,
                     team2=prediction.away_team_name,
                     event_date="",
                     first_team_cof=prediction.home_team_winning_percent,
                     second_team_cof=prediction.away_team_winning_percent,
                     draws_cof=prediction.draws_team_winning_percent,
                     advice=prediction.advice,
                     sent_to_user=False)\


    def to_prediction(self):
        prediction = Prediction()
        prediction.home_team_name = self.team1
        prediction.away_team_name = self.team2
        prediction.home_team_winning_percent = self.first_team_cof
        prediction.away_team_winning_percent = self.second_team_cof
        prediction.draws_team_winning_percent = self.draws_cof
        prediction.advice = self.advice
        return prediction

    def __eq__(self, other):
        return self.team1 == other.team1 and \
               self.team2 == other.team2


class EventDao:
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    def find_all(self):
        return self.session.query(Event).all()

    def event_for_teams_present(self, team1, team2):
        all = self.find_all()
        for event in all:
            lowers = [event.team1.lower(), event.team2.lower()]
            if team1.lower() in lowers and team2.lower() in lowers:
                return True
        return False

    def find_events_with_not_sent_flag(self):
        all = self.find_all()
        not_sent_events = list(filter(lambda x: not x.sent_to_user, all))
        return not_sent_events

    def pop_not_published_predictions(self):
        not_sent_events = self.find_events_with_not_sent_flag()
        for event in not_sent_events:
            event.sent_to_user = True
            flag_modified(event, 'sent_to_user')
            self.session.merge(event)
            self.session.commit()
        return list(map(lambda x: x.to_prediction(), not_sent_events))

    def pop_not_published_predictions_with_single_winner(self):
        not_sent_events = self.find_events_with_not_sent_flag()
        not_send_events_with_single_winner = list(filter(lambda x: x.to_prediction().has_single_winner(), not_sent_events))
        for event in not_send_events_with_single_winner:
            event.sent_to_user = True
            flag_modified(event, 'sent_to_user')
            self.session.merge(event)
            self.session.commit()
        return list(map(lambda x: x.to_prediction(), not_send_events_with_single_winner))

    def put_if_not_present(self, predictions):
        events = self.find_all()
        for prediction in predictions:
            event = Event.from_prediction(prediction)
            if event not in events:
                self.session.add(event)
                self.session.commit()
