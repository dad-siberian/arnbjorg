import json
import logging
import os

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)

from DialogFlow import detect_intent_texts, project_id


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger('Telegram Bot')


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f'Hi {user.mention_html()}!',
        reply_markup=ForceReply(selective=True),
    )


async def reply(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    text = detect_intent_texts(
        project_id, update.effective_chat.id, texts=update.message.text)
    await update.message.reply_text(text)


def main() -> None:
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(telegram_token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, reply))
    application.run_polling()


if __name__ == '__main__':
    main()
