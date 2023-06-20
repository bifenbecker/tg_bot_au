from __future__ import annotations
import messages
import logging
from pprint import pformat
from typing import TYPE_CHECKING
from telebot import types
from states import LeadState
from db.models import LeadAnswer
from db.orm import Session

if TYPE_CHECKING:
    from bot import Bot

logger = logging.getLogger(__name__)


class LeadContainer:
    bot: Bot
    current_state: LeadState
    data: dict

    def __init__(self, bot: Bot):
        self.bot = bot
        self.current_state = LeadState.LEAD_INIT_STATE
        self.data = {}
        self.bot.register_message_handler(self.set_region_name_handler,
                                          func=lambda
                                              message: self.current_state.name == LeadState.LEAD_SET_REGION_NAME.name)
        self.bot.register_callback_handler(self.set_set_business_info_handler,
                                           func=lambda
                                               message: self.current_state.name == LeadState.LEAD_SET_BUSINESS_INFO.name)
        self.bot.register_callback_handler(self.set_amount_clients_handler,
                                           func=lambda
                                               message: self.current_state.name == LeadState.LEAD_SET_AMOUNT_CLIENTS.name)
        self.bot.register_message_handler(self.set_telephone_handler,
                                           func=lambda
                                               message: self.current_state.name == LeadState.LEAD_SET_TELEPHONE.name)

    def entry(self, message: types.Message):
        self.set_state(next_state=LeadState.LEAD_SET_REGION_NAME, chat_id=message.chat.id)

    def set_region_name_handler(self, message: types.Message):
        logger.debug(f"STATE - {LeadState.LEAD_SET_REGION_NAME.name}. Message - {message.text}")
        self.data.update({
            "region_name": message.text
        })
        self.set_state(next_state=LeadState.LEAD_SET_BUSINESS_INFO, chat_id=message.chat.id)

    def set_set_business_info_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {LeadState.LEAD_SET_BUSINESS_INFO.name}. Message - {callback.data}")
        self.data.update({
            "business_info": callback.data
        })
        self.set_state(next_state=LeadState.LEAD_SET_AMOUNT_CLIENTS, chat_id=callback.message.chat.id)

    def set_amount_clients_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {LeadState.LEAD_SET_AMOUNT_CLIENTS.name}. Message - {callback.data}")
        self.data.update({
            "amount_clients": callback.data
        })
        self.set_state(next_state=LeadState.LEAD_SET_TELEPHONE,chat_id=callback.message.chat.id)

    def set_telephone_handler(self, message: types.Message):
        logger.debug(f"STATE - {LeadState.LEAD_SET_TELEPHONE.name}. Message - {message.text}")
        self.data.update({
            "telephone": message.text
        })
        logger.debug("FINAL DATA")
        logger.debug(pformat(self.data))
        self.show_message(text=messages.LEAD_FINAL, to=message.chat.id)
        try:
            with Session() as session:
                answer = LeadAnswer(**self.data, chat_id=message.chat.id)
                session.add(answer)
                session.commit()
        except Exception as e:
            logger.debug(e)
        self.set_state(next_state=LeadState.LEAD_INIT_STATE, chat_id=message.chat.id)

    def show_message(self, text: str, to: int):
        self.bot.send_message(text=text, to=to)

    def set_state(self, next_state: LeadState, chat_id: int):
        logger.debug(f"SET STATE - {next_state.name}")
        self.current_state = next_state
        if next_state != LeadState.LEAD_INIT_STATE:
            state_messages = {
                LeadState.LEAD_SET_REGION_NAME.name: messages.LEAD_SET_REGION_NAME,
                LeadState.LEAD_SET_BUSINESS_INFO.name: messages.LEAD_SET_BUSINESS_INFO,
                LeadState.LEAD_SET_AMOUNT_CLIENTS.name: messages.LEAD_SET_AMOUNT_CLIENTS,
                LeadState.LEAD_SET_TELEPHONE.name: messages.LEAD_SET_TELEPHONE,
            }
            state_keyboard = {
                LeadState.LEAD_SET_REGION_NAME.name: None,
                LeadState.LEAD_SET_BUSINESS_INFO.name: types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("Работаю один", callback_data="Работаю один"),
                    types.InlineKeyboardButton("Небольшой офис (до 5 человек)", callback_data="Небольшой офис (до 5 человек)"),
                    types.InlineKeyboardButton("Офис, 5-10 сотрудников", callback_data="Офис, 5-10 сотрудников"),
                    types.InlineKeyboardButton("Компания, до 20 сотрудников", callback_data="Компания, до 20 сотрудников"),
                    types.InlineKeyboardButton("Более 20 сотрудников", callback_data="Более 20 сотрудников"),
                ),
                LeadState.LEAD_SET_AMOUNT_CLIENTS.name: types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("До 5", callback_data="До 5"),
                    types.InlineKeyboardButton("До 10", callback_data="До 10"),
                    types.InlineKeyboardButton("До 25", callback_data="До 25"),
                    types.InlineKeyboardButton("До 50", callback_data="До 50"),
                    types.InlineKeyboardButton("От 50", callback_data="От 5"),
                ),
                LeadState.LEAD_SET_TELEPHONE.name: None
            }
            self.bot.send_message(to=chat_id, text=state_messages[self.current_state.name],
                                    reply_markup=state_keyboard[self.current_state.name])
