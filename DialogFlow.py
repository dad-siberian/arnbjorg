import json
import logging.config
import os

from dotenv import load_dotenv
from google.cloud import dialogflow

from log_config import LOGGING_CONFIG, TelegramLogsHandler

logger = logging.getLogger(__file__)


with open(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')) as file:
    project_id = json.load(file).get('project_id')


def detect_intent_texts(project_id, session_id, texts, language_code='ru-RU', is_fallback=True):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    for text in texts.split(' '):
        text_input = dialogflow.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        if is_fallback:
            return response.query_result.fulfillment_text
        else:
            if not response.query_result.intent.is_fallback:
                return response.query_result.fulfillment_text


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[
            message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.addHandler(TelegramLogsHandler(telegram_token, chat_id))
    with open('questions.json', 'r') as file:
        questions = json.load(file)
    for сaption in questions:
        display_name = сaption
        question = questions.get(сaption)
        training_phrases_parts = question.get('questions')
        message_texts = [question.get('answer')]
        try:
            create_intent(project_id, display_name,
                          training_phrases_parts, message_texts)
        except Exception as error:
            logger.exception(error)


if __name__ == '__main__':
    main()
