from crawler_api_integration.services import PredictionIntegrationService

service = PredictionIntegrationService()
predictions = service.get_predictions_for_new_matches()
for prediction in predictions:
    print(prediction)