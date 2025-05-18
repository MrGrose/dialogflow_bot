import logging
import random

import vk_api
from environs import Env
from telegram.ext import Updater
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow_bot import detect_intent_texts
from telegram_logger import TelegramLogsHandler

logger = logging.getLogger('Logger')


def send_vk_message(vk_bot, text, user_id):
    vk_bot.messages.send(
        user_id=user_id,
        message=text,
        random_id=random.randint(1, 1000)
    )


def main():
    env = Env()
    env.read_env()
    vk_token = env.str("VK_GROUP_TOKEN")
    project_id = env.str("PROJECT_ID")
    tg_token = env.str("TG_TOKEN")
    tg_chat_id = env.int("TG_CHAT_ID")

    vk_session = vk_api.VkApi(token=vk_token)
    vk_method_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    updater = Updater(token=tg_token)

    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(updater, tg_chat_id))

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                session_id = f"vk-{event.user_id}"
                response_text = detect_intent_texts(project_id, session_id, [event.text], "ru-RU")
                if response_text:
                    send_vk_message(vk_method_api, response_text, event.user_id)
    except Exception as error:
        logger.exception(f"VK бот упал с ошибкой:{error}")


if __name__ == '__main__':
    main()
