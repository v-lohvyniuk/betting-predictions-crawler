from flask import Flask, request
import os
import jsonpickle
from crawler_api_integration.services import PredictionIntegrationService
from crawler.crawlers import PariMatchCrawler
from footballapi.client import FootballApiClient
app = Flask(__name__)
__name__ = "__main__"


@app.route("/getPredictions")
def getPredictions():
    service = PredictionIntegrationService()
    predictions = service.get_matches_predictions()
    return jsonpickle.encode(predictions)


@app.route("/")
def hello():
    return "healthcheck is ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5201))
    app.run(host='0.0.0.0', port=port)