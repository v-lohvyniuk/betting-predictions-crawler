import schedule, time, threading


class Scheduler:

    def __init__(self):
        self.time = "10:30"

#   time like 10:30
    def every_day_at(self, time):
        self.time = time
        return self

    def execute(self, job):
        schedule.every().day.at(self.time).do(job)
        return self

    def __loop(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start(self):
        thread = threading.Thread(target=self.__loop)
        thread.daemon = True
        thread.start()