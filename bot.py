import telebot
from telebot import types
import typing
import logging

logger = logging.getLogger(__name__)


class Bot:
    _client: typing.Optional[telebot.TeleBot] = None

    def __init__(self, token: str):
        self._client = telebot.TeleBot(token=token)

        self._client.register_message_handler(self.on_text_handler)

    def on_text_handler(self, message: types.Message):
        logger.info(message)
        self._client.reply_to(message=message, text=message.text)

    def run(self):
        self._client.polling(none_stop=True)

    def process_new_updates(self, updates: list):
        self._client.process_new_updates(updates=updates)

    def remove_webhook(self):
        logger.info("Remove webhook")
        self._client.remove_webhook()

    def set_webhook(self, *args, **kwargs):
        logger.info("Set webhook")
        self._client.set_webhook(*args, **kwargs)


class BotFactory:
    __instance: typing.Optional[Bot] = None

    @classmethod
    def create_bot(cls, *args, **kwargs) -> Bot:
        if cls.__instance:
            return cls.__instance
        cls.__instance = Bot(*args, **kwargs)
        return cls.__instance
