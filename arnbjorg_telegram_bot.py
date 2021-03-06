import logging.config
import os

import google.auth
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from DialogFlow import detect_intent_texts
from log_config import LOGGING_CONFIG, TelegramLogsHandler

logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot assistant")


def reply(update: Update, context: CallbackContext):
    try:
        fulfillment_text = detect_intent_texts(
            project_id=google.auth.default()[1],
            session_id=update.effective_chat.id,
            text=update.message.text
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=fulfillment_text.get('fulfillment_text')
        )
    except Exception as error:
        logger.exception(error)


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')

    logging.config.dictConfig(LOGGING_CONFIG)
    logger.addHandler(TelegramLogsHandler(telegram_token, chat_id))

    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command), reply))
    logger.info('The arnbjorg Telegram Bot is running')
    updater.start_polling()


if __name__ == '__main__':
    main()
