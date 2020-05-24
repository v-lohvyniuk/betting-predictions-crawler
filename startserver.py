from flask import Flask, render_template
import os
import jsonpickle
from crawler_api_integration.services import PredictionIntegrationService
from crawler.crawlers import PariMatchCrawler
from footballapi.client import FootballApiClient
from footballapi.models import Prediction
app = Flask(__name__)
__name__ = "__main__"


@app.route("/getPredictions")
def getPredictions():
    service = PredictionIntegrationService(PariMatchCrawler(), FootballApiClient())
    predictions = service.get_matches_predictions()
    response = []
    for prediction in predictions:
        response.append("<p>" + prediction.__str__()  + "</pcookies>")
    return jsonpickle.encode(response)


@app.route("/getPredictionsAsTable")
def getPredictionsAsTable():
    service = PredictionIntegrationService(PariMatchCrawler(), FootballApiClient())
    predictions = service.get_matches_predictions()

    return render_template("predictions.html", predictions=predictions)

@app.route("/")
def hello():
    return "Hello world"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5201))
    app.run(host='0.0.0.0', port=port)