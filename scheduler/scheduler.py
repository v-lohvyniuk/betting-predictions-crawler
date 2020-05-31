import schedule, time, threading


class Scheduler:

    def __init__(self):
        self.mins = 1
        self.time = "10:30"

    def every_mins(self, mins):
        self.mins = mins
        return self

#   time like 10:30
    def every_day_at(self, time):
        self.time = time
        return self

    def execute(self, job):
        schedule.every(self.mins).minutes.do(job)
        return self

    def __loop(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start(self):
        thread = threading.Thread(target=self.__loop)
        thread.daemon = True
        thread.start()