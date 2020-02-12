import logging
import os
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow_intents import detect_intent_texts
from telegram_logger import TelegramLogsHandler

PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']
logger = logging.getLogger("dvmn_bot_vk")


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
    debug_bot_token = os.environ['DEBUG_BOT_TOKEN']
    debug_chat_id = os.environ['DEBUG_CHAT_ID']

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(
        debug_bot_token=debug_bot_token,
        chat_id=debug_chat_id,
    ))

    vk_session = vk_api.VkApi(token=vk_token)
    logger.info('Бот GAMEVERB_BOT в ВКонтакте запущен')

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            take_dialogflow_answer(event, vk_session.get_api())


if __name__ == "__main__":
    main()
