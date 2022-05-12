import logging
import os

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f'Hi {user.mention_html()}!',
        reply_markup=ForceReply(selective=True),
    )


async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == '__main__':
    main()
