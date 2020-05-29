import schedule, time, threading


class Scheduler:

    def __init__(self):
        self.mins = 1

    def every_mins(self, mins):
        self.mins = mins
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


# def log():
#     print("Hi this is it")
#
#
# scheduler = Scheduler()
# scheduler.every_mins(1).execute(log).start()
# input()