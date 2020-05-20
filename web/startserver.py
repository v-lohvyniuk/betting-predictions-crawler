from flask import Flask
import jsonpickle
from crawler_api_integration.services import PredictionIntegrationService
from crawler.crawlers import PariMatchCrawler
from footballapi.client import FootballApiClient
app = Flask(__name__)


@app.route("/getPredictions")
def getPredictions():
    service = PredictionIntegrationService(PariMatchCrawler(), FootballApiClient())
    predictions = service.get_matches_predictions()
    response = []
    for prediction in predictions:
        response.append(prediction.__str__())
    return jsonpickle.encode(response)


if __name__ == "__main__":
    app.run(port=5002)