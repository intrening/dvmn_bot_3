import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
import random
from dialogflow_intents import detect_intent_texts

PROJECT_ID = os.environ['PROJECT_ID']


def take_dialogflow_answer(event, vk_api):
    response = detect_intent_texts(
        project_id=PROJECT_ID,
        session_id=event.user_id,
        text=event.text,
    )
    if response.query_result.intent.is_fallback:
        return None
    vk_api.messages.send(
        user_id=event.user_id,
        message=response.query_result.fulfillment_text,
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
            take_dialogflow_answer(event, vk_session.get_api())


if __name__ == "__main__":
    main()
