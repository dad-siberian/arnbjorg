import logging.config
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from DialogFlow import detect_intent_texts, project_id
from log_config import LOGGING_CONFIG, TelegramLogsHandler

logger = logging.getLogger(__file__)


def reply(event, vk_api):
    message = detect_intent_texts(
        project_id, event.user_id, event.text, is_fallback=False)
    if message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    logging.config.dictConfig(LOGGING_CONFIG)
    logger.addHandler(TelegramLogsHandler(telegram_token, chat_id))

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info('The arnbjorg VkBot is running')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api)


if __name__ == '__main__':
    main()
