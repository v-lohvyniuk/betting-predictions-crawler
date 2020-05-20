from crawler_api_integration.services import PredictionIntegrationService
from crawler.crawlers import PariMatchCrawler
from footballapi.client import FootballApiClient

service = PredictionIntegrationService(PariMatchCrawler(), FootballApiClient())
predictions = service.get_matches_predictions()
for prediction in predictions:
    print(prediction)