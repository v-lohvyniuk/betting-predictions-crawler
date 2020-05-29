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
    predictions = service.get_matches_predictions()
    response = []
    for prediction in predictions:
        response.append("<p>" + prediction.__str__()  + "</pcookies>")
    return jsonpickle.encode(response)


@app.route("/getPredictionsAsTable")
def getPredictionsAsTable():
    service = PredictionIntegrationService()
    predictions = service.get_matches_predictions()

    return render_template("predictions.html", predictions=predictions)


@app.route("/")
def hello():
    return "<h1> </h2> Application is UP, all services are running"


if __name__ == "__main__":
    telegram_bot = TelegramBotService()
    telegram_bot.start_in_separate_thread()
    Scheduler().every_mins(1).execute(PredictionIntegrationService().get_matches_predictions).start()
    Scheduler().every_mins(2).execute(telegram_bot.send_new_predictions).start()
    port = int(os.environ.get("PORT", 5201))
    app.run(host='0.0.0.0', port=port)