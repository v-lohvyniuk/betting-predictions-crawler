import schedule, time, threading
from datetime import datetime


class Scheduler:

    def __init__(self):
        self.action = Scheduler.__print_ticking
        self.delay_from_start_min = 0

    @staticmethod
    def __print_ticking():
        print("Tick-tack ..." + str(datetime.now().time().minute))

    def do_action(self, action):
        self.action = action
        return self

    # time in format like "10:30"
    def start_at(self, time_str):
        self.start_time = time.strptime(time_str, "%H:%M")
        return self

    # time in format like "10:30"
    def end_at(self, time_str):
        self.end_time = time.strptime(time_str, "%H:%M")
        return self

    def delay_from_start(self, delay):
        self.delay_from_start_min = delay
        return self

    def every_minutes(self, minutes: int):
        self.delay = minutes
        return self

    def every_hours(self, hours: int):
        self.delay = hours*60
        return self

    def __current_time_matches_range(self):
        now = datetime.now().time()
        return self.start_time.tm_hour <= now.hour <= self.end_time.tm_hour

    def __run(self):
        while True:
            if self.__current_time_matches_range():
                thread = threading.Thread(target=self.action)
                thread.daemon = True
                thread.start()
            time.sleep(30*2*self.delay)
                
    def schedule(self):
        time.sleep(60 * self.delay_from_start_min)
        thread = threading.Thread(target=self.__run)
        thread.daemon = True
        thread.start()
