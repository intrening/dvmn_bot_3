import logging
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dialogflow_intents import detect_intent_texts

PROJECT_ID = os.environ['PROJECT_ID']
logger = logging.getLogger("dvmn_bot")


class MyLogsHandler(logging.Handler):
    def __init__(self, bot_token, chat_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.debug_bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.debug_bot.send_message(self.chat_id, text=log_entry)


def start(bot, update):
    update.message.reply_text('Здравствуйте!')


def take_dialogflow_answer(bot, update):
    answer = detect_intent_texts(
        project_id=PROJECT_ID,
        session_id=update.message.chat_id,
        text=update.message.text,
    )
    if answer:
        update.message.reply_text(answer)


def error(bot, update, error):
    global logger
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    gameverb_bot_token = os.environ['GAMEVERB_BOT_TOKEN']
    debug_bot_token = os.environ['DEBUG_BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']

    global logger
    logger.setLevel(logging.INFO)
    logger.addHandler(
        MyLogsHandler(
            bot_token=debug_bot_token,
            chat_id=chat_id,
        ),
    )

    updater = Updater(gameverb_bot_token)
    dispatcher = updater.dispatcher
    logger.info('Бот GAMEVERB_BOT запущен')

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    answer_handler = MessageHandler(Filters.text, take_dialogflow_answer)
    dispatcher.add_handler(answer_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
