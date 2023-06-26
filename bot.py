import telebot
import messages
import time
import logging
from telebot import types
from typing import Optional, Union
from containers import PartnerContainer, BflContainer, LeadContainer
from states import PartnerState, BflState, LeadState, MainState
from db.orm import Session
from db.models import StartRecord, User

logger = logging.getLogger(__name__)


class Bot:
    _client: Optional[telebot.TeleBot] = None
    _user: Optional[types.User] = None

    def __init__(self, token: str):
        self._client = telebot.TeleBot(token=token)
        self._user = None
        self.current_state = MainState.INIT

        self._client.set_my_commands([
            telebot.types.BotCommand("/start", "start"),
            telebot.types.BotCommand("/partner", "> Найти арбитражного управляющего для долгой работы"),
            telebot.types.BotCommand("/bfl", "> Найти арбитражного управляющего для конкретного банкрота"),
            telebot.types.BotCommand("/lead", "> Мне нужны Клиенты на банкротство!"),
        ])

        self._client.register_message_handler(self.on_start_handler, func=lambda message: self.current_state.name != MainState.START.name, commands=["start"])
        self._client.register_message_handler(self.on_partner_handler, func=lambda message: self.current_state.name != MainState.START.name, commands=["partner"])
        self._client.register_message_handler(self.on_bfl_handler, func=lambda message: self.current_state.name != MainState.START.name, commands=["bfl"])
        self._client.register_message_handler(self.on_lead_handler, func=lambda message: self.current_state.name != MainState.START.name, commands=["lead"])
        self._client.register_callback_query_handler(self.on_callback_handler, func=lambda
            message: self.current_state.name == MainState.START.name)

    @property
    def user(self) -> types.User:
        return self._user

    def save_record(self, message: types.Message):
        try:
            with Session() as session:
                user = session.query(User).filter(User.telegram_id == message.chat.id).one_or_none()
                if not user:
                    user = User(
                        telegram_id=message.chat.id,
                        username=message.from_user.username
                    )
                    session.add(user)
                record = StartRecord(
                    chat_id=message.chat.id,
                    username=message.from_user.username,
                )
                session.add(record)
                session.commit()
        except Exception as e:
            logger.error(e)

    def on_callback_handler(self, callback: types.CallbackQuery):
        command_type = callback.data
        actions = {
            "partner": self.on_partner_handler,
            "bfl": self.on_bfl_handler,
            "lead": self.on_lead_handler,
        }
        action = actions.get(command_type, None)
        if action:
            action(message=callback.message)

    def on_start_handler(self, message: types.Message):
        logger.info("/START command")
        logger.debug(message)
        self.current_state = MainState.START
        self.save_record(message=message)
        self.send_message(to=message.chat.id, text=messages.START_COMMAND_HELLO)
        sleep = 5
        logger.debug(f"SLEEP {sleep}s")
        time.sleep(sleep)
        self.send_message(to=message.chat.id, text=messages.START_COMMAND_DESCRIPTION,
                          reply_markup=types.InlineKeyboardMarkup().add(
                              types.InlineKeyboardButton(
                                  text="Найти арбитражного управляющего для долгой работы (/partner)",
                                  callback_data="partner"),
                              types.InlineKeyboardButton(
                                  text="Найти арбитражного управляющего для конкретного банкрота (/bfl)",
                                  callback_data="bfl"),
                              types.InlineKeyboardButton(
                                  text="Я сам АУ (или юрист) и мне нужны клиенты на бфл! (/lead)",
                                  callback_data="lead"),
                          ))
        self.current_state = MainState.INIT

    def on_partner_handler(self, message: types.Message):
        logger.info("/PARTNER command")
        logger.debug(message)
        self.save_record(message=message)
        self.current_state = PartnerState.PARTNER_INIT_STATE
        partner_container = PartnerContainer(bot=self)
        partner_container.entry(message=message)

    def on_bfl_handler(self, message: types.Message):
        logger.info("/BFL command")
        logger.debug(message)
        self.save_record(message=message)
        self.current_state = BflState.BFL_INIT_STATE
        bfl_container = BflContainer(bot=self)
        bfl_container.entry(message=message)

    def on_lead_handler(self, message: types.Message):
        logger.info("/LEAD command")
        logger.debug(message)
        self.save_record(message=message)
        self.current_state = LeadState.LEAD_INIT_STATE
        lead_container = LeadContainer(bot=self)
        lead_container.entry(message=message)

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
