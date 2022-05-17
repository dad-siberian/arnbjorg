import logging
import json
import os

from google.cloud import dialogflow


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger('Create intent')


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
    with open('questions.json', 'r') as file:
        questions = json.load(file)
    with open(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')) as file:
        project_id = json.load(file).get('project_id')
    for question in questions:
        display_name = question
        q = questions[question]  # RENAME
        training_phrases_parts = q.get('questions')
        message_texts = [q.get('answer')]
        create_intent(project_id, display_name,
                      training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()
