import requests, threading
from crawler_api_integration.services import PredictionIntegrationService
url = "https://api.telegram.org/bot1047441785:AAHsmgHh3gAl0A1k5ljO8qcdN8ixN6iS-SU/"


class TelegramClient:

    def get_updates_json(self, request):
        params = {'timeout': 100, 'offset': None}
        response = requests.get(request + "getUpdates", data=params)
        return response.json()

    def last_update(self, data):
        results = data['result']
        total_updates = len(results) - 1
        return results[total_updates]

    def get_chat_id(self, update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def send_mess(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(url + 'sendMessage', data=params)
        return response


class TelegramBotService:

    def __init__(self):
        self.client = TelegramClient()

    def main(self):
        next_update_id = self.client.last_update(self.client.get_updates_json(url))['update_id'] + 1
        while True:
            update = self.client.last_update(self.client.get_updates_json(url))
            if next_update_id == update['update_id']:
                next_update_id = next_update_id + 1

                message = update['message']['text']
                chat_id = self.client.get_chat_id(update)
                if message.lower() in "all":
                    self.client.send_mess(chat_id, "Yep, processing ...")
                    prediction_service = PredictionIntegrationService()
                    predictions = prediction_service.get_matches_predictions()
                    for prediction in predictions:
                        self.client.send_mess(chat_id, prediction.__str__())

                elif message.lower() in "winners":
                    self.client.send_mess(chat_id, "Yep, processing ...")
                    prediction_service = PredictionIntegrationService()
                    predictions = prediction_service.get_predictions_with_single_winner()
                    for prediction in predictions:
                        self.client.send_mess(chat_id, prediction.__str__())

                self.client.send_mess(chat_id, "You're all set !\nIf I'm not responding start me using going on\n https://pari-match-predictions-crawler.herokuapp.com/")

    def start_in_separate_thread(self):
        thread = threading.Thread(target=TelegramBotService.main, args=[self])
        thread.daemon = True
        thread.start()

