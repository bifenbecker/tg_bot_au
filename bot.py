import telebot
import messages
import time
import logging
from telebot import types
from typing import Optional, Union
from containers import PartnerContainer, BflContainer, LeadContainer
from db.orm import Session
from db.models import StartRecord

logger = logging.getLogger(__name__)


class Bot:
    _client: Optional[telebot.TeleBot] = None
    _user: Optional[types.User] = None

    def __init__(self, token: str):
        self._client = telebot.TeleBot(token=token)
        self._user = None

        self._client.set_my_commands([
            telebot.types.BotCommand("/start", "start"),
            telebot.types.BotCommand("/partner", "> Найти арбитражного управляющего для долгой работы"),
            telebot.types.BotCommand("/bfl", "> Найти арбитражного управляющего для конкретного банкрота"),
            telebot.types.BotCommand("/lead", "> Мне нужны Клиенты на банкротство!"),
        ])

        self._client.register_message_handler(self.on_start_handler, commands=["start"])
        self._client.register_message_handler(self.on_partner_handler, commands=["partner"])
        self._client.register_message_handler(self.on_bfl_handler, commands=["bfl"])
        self._client.register_message_handler(self.on_lead_handler, commands=["lead"])

    @property
    def user(self) -> types.User:
        return self._user

    def save_record(self):
        with Session() as session:
            record = StartRecord(
                chat_id=self._user.id,
                username=self._user.username,
            )
            session.add(record)
            session.commit()

    def on_start_handler(self, message: types.Message):
        if not self._user:
            self._user = message.from_user
        logger.info("/START command")
        logger.debug(message)
        self.save_record()
        self.send_reply_message(text=messages.START_COMMAND_HELLO)
        sleep = 5
        logger.debug(f"SLEEP {sleep}s")
        time.sleep(sleep)
        self.send_reply_message(text=messages.START_COMMAND_DESCRIPTION)

    def on_partner_handler(self, message: types.Message):
        if not self._user:
            self._user = message.from_user
        logger.info("/PARTNER command")
        logger.debug(message)
        self.save_record()
        partner_container = PartnerContainer(bot=self)
        partner_container.entry()

    def on_bfl_handler(self, message: types.Message):
        if not self._user:
            self._user = message.from_user
        logger.info("/BFL command")
        logger.debug(message)
        self.save_record()
        bfl_container = BflContainer(bot=self)
        bfl_container.entry()

    def on_lead_handler(self, message: types.Message):
        if not self._user:
            self._user = message.from_user
        logger.info("/LEAD command")
        logger.debug(message)
        lead_container = LeadContainer(bot=self)
        lead_container.entry()

    def send_message(self, to: Union[str, int], text: str, **kwargs):
        logger.debug(f"Send message - {text} to {to}")
        self._client.send_message(chat_id=to, text=text, parse_mode='Markdown', **kwargs)

    def send_reply_message(self, text: str, **kwargs):
        if self._user:
            self.send_message(to=self._user.id, text=text, **kwargs)
        else:
            logger.error("No loaded user")
            raise Exception("No loaded user")

    def register_message_handler(self, *args, **kwargs):
        self._client.register_message_handler(*args, **kwargs)

    def register_callback_handler(self, *args, **kwargs):
        self._client.register_callback_query_handler(*args, **kwargs)

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
