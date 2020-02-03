import os
import logging
import telegram


class TelegramLogsHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug_bot = telegram.Bot(token=os.environ['DEBUG_BOT_TOKEN'])
        self.chat_id = os.environ['DEBUG_CHAT_ID']

    def emit(self, record):
        log_entry = self.format(record)
        self.debug_bot.send_message(self.chat_id, text=log_entry)
