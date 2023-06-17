from __future__ import annotations
import messages
import logging
from pprint import pformat
from typing import Optional, TYPE_CHECKING
from telebot import types
from states import BflState

if TYPE_CHECKING:
    from bot import Bot

logger = logging.getLogger(__name__)


class BflContainer:
    bot: Bot
    current_state: BflState
    data: dict

    def __init__(self, bot: Bot):
        self.bot = bot
        self.current_state = BflState.BFL_INIT_STATE
        self.data = {}
        self.bot.register_message_handler(self.set_region_name_handler,
                                          func=lambda
                                              message: self.current_state.name == BflState.BFL_SET_REGION_NAME.name)
        self.bot.register_message_handler(self.set_insolvent_situation_handler,
                                          func=lambda
                                              message: self.current_state.name == BflState.BFL_SET_INSOLVENT_SITUATION.name)
        self.bot.register_callback_handler(self.set_amount_expense_handler,
                                           func=lambda
                                               message: self.current_state.name == BflState.BFL_SET_AMOUNT_EXPENSE.name)
        self.bot.register_callback_handler(self.set_guarantees_handler,
                                           func=lambda
                                               message: self.current_state.name == BflState.BFL_SET_GUARANTEES.name)
        self.bot.register_callback_handler(self.set_experience_handler,
                                           func=lambda
                                               message: self.current_state.name == BflState.BFL_SET_EXPERIENCE.name)
        self.bot.register_message_handler(self.set_telephone_handler,
                                          func=lambda
                                              message: self.current_state.name == BflState.BFL_SET_TELEPHONE.name)

    def entry(self):
        self.set_state(next_state=BflState.BFL_SET_REGION_NAME)

    def set_region_name_handler(self, message: types.Message):
        logger.debug(f"STATE - {BflState.BFL_SET_REGION_NAME.name}. Message - {message.text}")
        self.data.update({
            "region_name": message.text
        })
        self.set_state(next_state=BflState.BFL_SET_INSOLVENT_SITUATION)

    def set_insolvent_situation_handler(self, message: types.Message):
        logger.debug(f"STATE - {BflState.BFL_SET_INSOLVENT_SITUATION.name}. Message - {message.text}")
        self.data.update({
            "insolvent_situation": message.text
        })
        self.set_state(next_state=BflState.BFL_SET_AMOUNT_EXPENSE)

    def set_amount_expense_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {BflState.BFL_SET_AMOUNT_EXPENSE.name}. Message - {callback.data}")
        self.data.update({
            "amount_expense": callback.data
        })
        self.set_state(next_state=BflState.BFL_SET_GUARANTEES)

    def set_guarantees_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {BflState.BFL_SET_GUARANTEES.name}. Message - {callback.data}")
        self.data.update({
            "guarantees": callback.data
        })
        self.set_state(next_state=BflState.BFL_SET_EXPERIENCE)

    def set_experience_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {BflState.BFL_SET_EXPERIENCE.name}. Message - {callback.data}")
        self.data.update({
            "experience": callback.data
        })
        self.set_state(next_state=BflState.BFL_SET_TELEPHONE)

    def set_telephone_handler(self, message: types.Message):
        logger.debug(f"STATE - {BflState.BFL_SET_TELEPHONE.name}. Message - {message.text}")
        self.data.update({
            "telephone": message.text
        })
        logger.debug("FINAL DATA")
        logger.debug(pformat(self.data))
        self.show_message(text=messages.PARTNER_FINAL)
        self.set_state(next_state=BflState.BFL_INIT_STATE)

    def show_message(self, text: str):
        self.bot.send_reply_message(text=text)

    def set_state(self, next_state: BflState):
        logger.debug(f"SET STATE - {next_state.name}")
        self.current_state = next_state
        if next_state != BflState.BFL_INIT_STATE:
            state_messages = {
                BflState.BFL_SET_REGION_NAME.name: messages.BFL_SET_REGION_NAME,
                BflState.BFL_SET_INSOLVENT_SITUATION.name: messages.BFL_SET_INSOLVENT_SITUATION,
                BflState.BFL_SET_AMOUNT_EXPENSE.name: messages.BFL_SET_AMOUNT_EXPENSE,
                BflState.BFL_SET_GUARANTEES.name: messages.BFL_SET_GUARANTEES,
                BflState.BFL_SET_EXPERIENCE.name: messages.BFL_SET_EXPERIENCE,
                BflState.BFL_SET_TELEPHONE.name: messages.BFL_SET_TELEPHONE,
            }
            state_keyboard = {
                BflState.BFL_SET_REGION_NAME.name: None,
                BflState.BFL_SET_INSOLVENT_SITUATION.name: None,
                BflState.BFL_SET_AMOUNT_EXPENSE.name: types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("до 50 000 руб.", callback_data="до 50 000 руб."),
                    types.InlineKeyboardButton("до 60 000 руб.", callback_data="до 60 000 руб."),
                    types.InlineKeyboardButton("до 70 000 руб.", callback_data="до 70 000 руб."),
                    types.InlineKeyboardButton("Цена не важна", callback_data="Цена не важна"),
                ),
                BflState.BFL_SET_GUARANTEES.name: types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("Гарантии нужны", callback_data="Гарантии нужны"),
                    types.InlineKeyboardButton("Гарантии не нужны", callback_data="Гарантии не нужны"),
                    types.InlineKeyboardButton("Пока не определился", callback_data="Пока не определился"),
                ),
                BflState.BFL_SET_EXPERIENCE.name: types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("Можно без опыта", callback_data="Можно без опыта"),
                    types.InlineKeyboardButton("До 50 завершенных дел", callback_data="До 50 завершенных дел"),
                    types.InlineKeyboardButton("От 50 до 200 завершенных дел",
                                               callback_data="От 50 до 200 завершенных дел"),
                    types.InlineKeyboardButton("От 200 до 1000 завершенных дел",
                                               callback_data="От 200 до 1000 завершенных дел"),
                    types.InlineKeyboardButton("Более 1000 завершенных дел", callback_data="Более 1000 завершенных дел"),
                ),
                BflState.BFL_SET_TELEPHONE.name: None,
            }
            self.bot.send_reply_message(text=state_messages[self.current_state.name],
                                    reply_markup=state_keyboard[self.current_state.name])
