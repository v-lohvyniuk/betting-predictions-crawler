from crawler_api_integration.services import PredictionIntegrationService

service = PredictionIntegrationService()
predictions = service.get_matches_predictions()
for prediction in predictions:
    print(prediction)