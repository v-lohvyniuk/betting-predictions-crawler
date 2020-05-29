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

    def get_last_update(self):
        data = self.get_updates_json(url)
        return self.last_update(data)

    def get_last_update_id(self):
        return self.get_last_update()['update_id']

    def get_chat_id(self, update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def get_message_text(self, update):
        text = update['message']['text']
        return text

    def send_mess(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(url + 'sendMessage', data=params)
        return response


class BotKeywords:
    ALL = "all"
    WIN = "win"
    WINNERS = "winners"

    @staticmethod
    def as_list():
        return [BotKeywords.ALL, BotKeywords.WIN, BotKeywords.WINNERS]


class TelegramBotService:

    def __init__(self):
        self.client = TelegramClient()
        self.next_update_id = self.client.get_last_update_id() + 1

    @staticmethod
    def is_reserved_keyword(keyword):
        return keyword.lower() in BotKeywords.as_list()

    def is_new_update(self, update):
        return self.next_update_id == update['update_id']

    def respond_to_command(self, chat_id, command_keyword):
        self.client.send_mess(chat_id, "Gathering data ...")
        prediction_service = PredictionIntegrationService()
        result_list = []
        if command_keyword.lower() in BotKeywords.ALL:
            result_list = prediction_service.get_matches_predictions()
        elif command_keyword.lower() in [BotKeywords.WINNERS, BotKeywords.WIN]:
            result_list = prediction_service.get_predictions_with_single_winner()

        for prediction in result_list:
            self.client.send_mess(chat_id, prediction.__str__())

        self.client.send_mess(chat_id, f"Results found: {len(result_list)}")

    def send_default_failure_message(self, chat_id):
        self.client.send_mess(chat_id, "Cannot parse your request\n"
                                       "Try use one of keywords {}".format(BotKeywords.as_list()))

    def process_update(self, update):
        message = self.client.get_message_text(update)
        chat_id = self.client.get_chat_id(update)
        if self.is_reserved_keyword(message):
            self.respond_to_command(chat_id, message)
        else:
            self.send_default_failure_message(chat_id)

    def main(self):
        while True:
            update = self.client.get_last_update()
            if self.is_new_update(update):
                self.next_update_id += 1
                self.process_update(update)

    def start_in_separate_thread(self):
        thread = threading.Thread(target=TelegramBotService.main, args=[self])
        thread.daemon = True
        thread.start()

