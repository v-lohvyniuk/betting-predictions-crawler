from crawler_api_integration.services import PredictionIntegrationService

service = PredictionIntegrationService()
predictions = service.get_and_persist_predictions()
for prediction in predictions:
    print(prediction)