import logging, os, telegram
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
        MyLogsHandler(bot_token=os.environ['DEBUG_BOT_TOKEN'],
        chat_id=CHAT_ID)
    )

    bot = telegram.Bot(token=GAMEVERB_BOT_TOKEN)
    logger.info('Бот GAMEVERB_BOT запущен')

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(GAMEVERB_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    # while True:
    #     try:
    #         text = 'eer'
    #         bot.send_message(chat_id=CHAT_ID, text=text)
    #     except requests.exceptions.ReadTimeout:
    #         pass
    #     except requests.exceptions.ConnectionError:
    #         time.sleep(10)
    #     except Exception as err:
    #         logger.error(err, exc_info=True)

if __name__ == "__main__":
    main()