import telebot
import messages
import time
from telebot import types
from typing import Optional, Union
import logging

logger = logging.getLogger(__name__)


class Bot:
    _client: Optional[telebot.TeleBot] = None
    _user: Optional[types.User] = None

    def __init__(self, token: str):
        self._client = telebot.TeleBot(token=token)
        self._user = None

        self._client.set_my_commands([
            telebot.types.BotCommand("/start", "start"),
        ])

        self._client.register_message_handler(self.on_start_handler, commands=["start"])
        self._client.register_message_handler(self.on_text_handler, content_types=["text"])

    def on_text_handler(self, message: types.Message):
        if not self._user:
            self._user = message.from_user
        logger.info(message)
        self._client.reply_to(message=message, text=message.text)

    def on_start_handler(self, message: types.Message):
        if not self._user:
            self._user = message.from_user
        logger.info("/START command")
        logger.debug(message)
        self.send_reply_message(text=messages.START_COMMAND_HELLO)
        sleep = 5
        logger.debug(f"SLEEP {sleep}s")
        time.sleep(sleep)
        self.send_reply_message(text=messages.START_COMMAND_DESCRIPTION)

    def send_message(self, to: Union[str, int], text: str):
        logger.debug(f"Send message - {text} to {to}")
        self._client.send_message(chat_id=to, text=text)

    def send_reply_message(self, text: str):
        if self._user:
            self.send_message(to=self._user.id, text=text)
        else:
            logger.error("No loaded user")
            raise Exception("No loaded user")

    def run(self):
        self._client.polling(none_stop=True)

    def process_new_updates(self, updates: list):
        self._client.process_new_updates(updates=updates)

    def remove_webhook(self):
        logger.debug("Remove webhook")
        self._client.remove_webhook()

    def set_webhook(self, *args, **kwargs):
        logger.debug("Set webhook")
        self._client.set_webhook(*args, **kwargs)


class BotFactory:
    __instance: Optional[Bot] = None

    @classmethod
    def create_bot(cls, *args, **kwargs) -> Bot:
        if cls.__instance:
            return cls.__instance
        cls.__instance = Bot(*args, **kwargs)
        return cls.__instance
