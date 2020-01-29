import logging
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


GAMEVERB_BOT_TOKEN = os.environ['GAMEVERB_BOT_TOKEN']
DEBUG_BOT_TOKEN = os.environ['DEBUG_BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

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


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


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

    # bot = telegram.Bot(token=GAMEVERB_BOT_TOKEN)

    updater = Updater(GAMEVERB_BOT_TOKEN)
    dispatcher = updater.dispatcher
    logger.info('Бот GAMEVERB_BOT запущен')

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
