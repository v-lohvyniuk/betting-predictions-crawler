from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from footballapi.models import Prediction

Base = declarative_base()
user="gtvdrkjgsvphfm"
password="14eb59e2296723ea6865c1cd6abf1c8acad0f3f92fe99674d42cc62961116f85"
host="ec2-54-246-90-10.eu-west-1.compute.amazonaws.com"
port="5432"
database="dbhribebhu9rel"


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
                     sent_to_user=False)

    def eq(self, prediction: Prediction):
        return self.team1 == prediction.home_team_name and \
               self.team2 == prediction.away_team_name


class EventDao:
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    def find_all(self):
        return self.session.query(Event).all()

    def put_if_not_present(self, predictions):
        events = self.find_all()
        for prediction in predictions:
            event = Event.from_prediction(prediction)
            if event not in events:
                self.session.add(event)
                self.session.commit()
