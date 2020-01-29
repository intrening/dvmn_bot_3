import logging
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import dialogflow_v2 as dialogflow

GAMEVERB_BOT_TOKEN = os.environ['GAMEVERB_BOT_TOKEN']
DEBUG_BOT_TOKEN = os.environ['DEBUG_BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
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
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def detect_intent_texts(project_id, session_id, text, language_code='ru-RU'):
    """Returns the result of detect intent with text as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    return (response.query_result.fulfillment_text)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def take_dialogflow_answer(bot, update):
    """Echo the user message."""
    answer = detect_intent_texts(
        project_id=PROJECT_ID,
        session_id=update.message.chat_id,
        text=update.message.text,
    )
    update.message.reply_text(answer)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    global logger
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    global logger
    logger.setLevel(logging.INFO)
    logger.addHandler(
        MyLogsHandler(
            bot_token=os.environ['DEBUG_BOT_TOKEN'],
            chat_id=CHAT_ID,
        ),
    )

    updater = Updater(GAMEVERB_BOT_TOKEN)
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
