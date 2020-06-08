from flask import Flask, render_template
import os
import jsonpickle
from crawler_api_integration.services import PredictionIntegrationService
from scheduler.scheduler import Scheduler
from telegram.client import TelegramBotService
from crawler.crawlers import PariMatchCrawler
app = Flask(__name__)
__name__ = "__main__"


@app.route("/getPredictions")
def getPredictions():
    service = PredictionIntegrationService()
    predictions = service.get_predictions_for_new_matches()
    response = []
    for prediction in predictions:
        response.append("<p>" + prediction.__str__()  + "</pcookies>")
    return jsonpickle.encode(response)


@app.route("/login")
def getLogin():
    return str(PariMatchCrawler().is_logged_in())


@app.route("/getPredictionsAsTable")
def getPredictionsAsTable():
    service = PredictionIntegrationService()
    predictions = service.get_predictions_for_new_matches()

    return render_template("predictions.html", predictions=predictions)


@app.route("/")
def hello():
    return "<h1> Application is UP, all services are running </h1>"


if __name__ == "__main__":
    telegram_bot = TelegramBotService()
    telegram_bot.start_in_separate_thread()
    delay = 120
    Scheduler()\
        .with_timezone(2)\
        .start_at("10:00").end_at("23:00")\
        .every_hours(2)\
        .do_action(PredictionIntegrationService().get_predictions_for_new_matches_with_single_winner)\
        .schedule()
    Scheduler()\
        .with_timezone(2)\
        .start_at("10:00").end_at("23:00")\
        .every_hours(2)\
        .delay_from_start(2)\
        .do_action(telegram_bot.send_new_predictions_wihth_single_winenr).schedule()

    port = int(os.environ.get("PORT", 5201))
    app.run(host='0.0.0.0', port=port)