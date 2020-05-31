import schedule, time, threading
import datetime


class Scheduler:

    def __init__(self):
        self.mins = 1

    def every_mins(self, mins):
        self.mins = mins
        return self

    @staticmethod
    def __get_now():
        return datetime.datetime.now()

    @staticmethod
    def get_todays_10_AM():
        return Scheduler.__get_now().replace(hour=10, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_todays_10_PM():
        return Scheduler.__get_now().replace(hour=22, minute=0, second=0, microsecond=0)

    def execute(self, job):
        schedule.every(self.mins).minutes.do(job)
        return self

    def __loop(self):
        while True:
            if Scheduler.get_todays_10_AM() < Scheduler.__get_now() < Scheduler.get_todays_10_PM():
                schedule.run_pending()
            time.sleep(1)

    def start(self):
        thread = threading.Thread(target=self.__loop)
        thread.daemon = True
        thread.start()