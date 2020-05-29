from flask import Flask, render_template
import os
import jsonpickle
from crawler_api_integration.services import PredictionIntegrationService
from scheduler.scheduler import Scheduler
from telegram.client import TelegramBotService
app = Flask(__name__)
__name__ = "__main__"


@app.route("/getPredictions")
def getPredictions():
    service = PredictionIntegrationService()
    predictions = service.get_and_persist_predictions()
    response = []
    for prediction in predictions:
        response.append("<p>" + prediction.__str__()  + "</pcookies>")
    return jsonpickle.encode(response)


@app.route("/getPredictionsAsTable")
def getPredictionsAsTable():
    service = PredictionIntegrationService()
    predictions = service.get_and_persist_predictions()

    return render_template("predictions.html", predictions=predictions)


@app.route("/")
def hello():
    return "<h1> </h2> Application is UP, all services are running"


if __name__ == "__main__":
    cron_param = 240
    telegram_bot = TelegramBotService()
    telegram_bot.start_in_separate_thread()
    Scheduler().every_mins(cron_param).execute(PredictionIntegrationService().get_and_persist_predictions).start()
    Scheduler().every_mins(cron_param + 3).execute(telegram_bot.send_new_predictions).start()
    port = int(os.environ.get("PORT", 5201))
    app.run(host='0.0.0.0', port=port)