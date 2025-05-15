import random

import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from dialog_flow_bot import detect_intent_texts


def send_vk(vk_bot, text, user_id):
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
    vk_session = vk_api.VkApi(token=vk_token)
    vk_method_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                result = detect_intent_texts(project_id, event.user_id, [event.text], "ru-RU")
                if result:
                    send_vk(vk_method_api, result, event.user_id)


if __name__ == '__main__':
    main()
