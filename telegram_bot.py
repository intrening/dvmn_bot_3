import logging
from telegram_logger import TelegramLogsHandler
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dialogflow_intents import detect_intent_texts

PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']
logger = logging.getLogger("dvmn_bot_telegram")


def start(bot, update):
    update.message.reply_text('Здравствуйте!')


def take_dialogflow_answer(bot, update):
    response = detect_intent_texts(
        project_id=PROJECT_ID,
        session_id=update.message.chat_id,
        text=update.message.text,
    )
    update.message.reply_text(
        response.query_result.fulfillment_text,
    )


def main():
    gameverb_bot_token = os.environ['GAMEVERB_BOT_TOKEN']

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler())

    updater = Updater(gameverb_bot_token)
    dispatcher = updater.dispatcher
    logger.info('Бот GAMEVERB_BOT в Telegram запущен')

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    answer_handler = MessageHandler(Filters.text, take_dialogflow_answer)
    dispatcher.add_handler(answer_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
