import logging
import os
import json

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)
from google.cloud import dialogflow


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
    with open(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')) as file: # Грязь
        project_id = json.load(file).get('project_id')
    text = detect_intent_texts(project_id, update.effective_chat.id, texts=update.message.text)
    await update.message.reply_text(text)


def detect_intent_texts(project_id, session_id, texts, language_code='ru-RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    #print("Session path: {}\n".format(session))
    for text in texts.split(' '):
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        # print("=" * 20)
        # print("Query text: {}".format(response.query_result.query_text))
        # print(
        #     "Detected intent: {} (confidence: {})\n".format(
        #         response.query_result.intent.display_name,
        #         response.query_result.intent_detection_confidence,
        #     )
        # )
        # print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        return response.query_result.fulfillment_text


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
