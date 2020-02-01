import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
import random
# from dialogflow_intents import detect_intent_texts


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000),
    )


def main():
    vk_token = os.environ['VK_GROUP_TOKEN']
    vk_session = vk_api.VkApi(token=vk_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_session.get_api())


if __name__ == "__main__":
    main()
