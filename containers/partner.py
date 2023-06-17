from __future__ import annotations

import messages
import logging
from typing import Optional, TYPE_CHECKING
from telebot import types
from states import PartnerState

if TYPE_CHECKING:
    from bot import Bot

logger = logging.getLogger(__name__)


class PartnerContainer:
    bot: Bot
    current_state: Optional[PartnerState] = None
    data: dict

    def __init__(self, bot: Bot):
        self.bot = bot
        self.current_state = None
        self.data = {}
        self.bot.register_message_handler(self.set_region_name_handler,
                                          func=lambda
                                              message: self.current_state.name == PartnerState.SET_REGION_NAME.name)
        self.bot.register_callback_handler(self.set_amount_deals_handler,
                                           func=lambda
                                               message: self.current_state.name == PartnerState.SET_AMOUNT_DEALS.name)
        self.bot.register_callback_handler(self.set_amount_expense_handler,
                                           func=lambda
                                               message: self.current_state.name == PartnerState.SET_AMOUNT_EXPENSE.name)
        self.bot.register_callback_handler(self.set_guarantees_handler,
                                           func=lambda
                                               message: self.current_state.name == PartnerState.SET_GUARANTEES.name)
        self.bot.register_callback_handler(self.set_experience_handler,
                                           func=lambda
                                               message: self.current_state.name == PartnerState.SET_EXPERIENCE.name)

    def entry(self):
        self.set_state(next_state=PartnerState.SET_REGION_NAME)

    def set_region_name_handler(self, message: types.Message):
        logger.debug(f"STATE - {PartnerState.SET_REGION_NAME.name}. Message - {message.text}")
        self.data.update({
            "region_name": message.text
        })
        self.set_state(next_state=PartnerState.SET_AMOUNT_DEALS)

    def set_amount_deals_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {PartnerState.SET_AMOUNT_DEALS.name}. Message - {callback.data}")
        self.data.update({
            "amount_deals": callback.data
        })
        self.set_state(next_state=PartnerState.SET_AMOUNT_EXPENSE)

    def set_amount_expense_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {PartnerState.SET_AMOUNT_EXPENSE.name}. Message - {callback.data}")
        self.data.update({
            "amount_expense": callback.data
        })
        self.set_state(next_state=PartnerState.SET_GUARANTEES)

    def set_guarantees_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {PartnerState.SET_GUARANTEES.name}. Message - {callback.data}")
        self.data.update({
            "guarantees": callback.data
        })
        self.set_state(next_state=PartnerState.SET_EXPERIENCE)

    def set_experience_handler(self, callback: types.CallbackQuery):
        logger.debug(f"STATE - {PartnerState.SET_EXPERIENCE.name}. Message - {callback.data}")
        self.data.update({
            "experience": callback.data
        })
        logger.debug("FINAL DATA ", self.data)
        self.show_message(text=messages.PARTNER_FINAL)

    def show_message(self, text: str):
        self.bot.send_reply_message(text=text)

    def set_state(self, next_state: PartnerState):
        logger.debug(f"SET STATE - {next_state.name}")
        self.current_state = next_state
        state_messages = {
            PartnerState.SET_REGION_NAME.name: messages.PARTNER_SET_REGION_NAME,
            PartnerState.SET_AMOUNT_DEALS.name: messages.PARTNER_SET_AMOUNT_DEALS,
            PartnerState.SET_AMOUNT_EXPENSE.name: messages.PARTNER_SET_AMOUNT_EXPENSE,
            PartnerState.SET_GUARANTEES.name: messages.PARTNER_SET_GUARANTEES,
            PartnerState.SET_EXPERIENCE.name: messages.PARTNER_SET_EXPERIENCE,
        }
        state_keyboard = {
            PartnerState.SET_REGION_NAME.name: None,
            PartnerState.SET_AMOUNT_DEALS.name: types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("до 5", callback_data="до 5"),
                types.InlineKeyboardButton("до 10", callback_data="до 10"),
                types.InlineKeyboardButton("до 20", callback_data="до 20"),
                types.InlineKeyboardButton("до 50", callback_data="до 50"),
                types.InlineKeyboardButton("более 50", callback_data="более 5"),
            ),
            PartnerState.SET_AMOUNT_EXPENSE.name: types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("до 50 000 руб.", callback_data="до 50 000 руб."),
                types.InlineKeyboardButton("до 60 000 руб.", callback_data="до 60 000 руб."),
                types.InlineKeyboardButton("до 70 000 руб.", callback_data="до 70 000 руб."),
                types.InlineKeyboardButton("Цена не важна", callback_data="Цена не важна"),
            ),
            PartnerState.SET_GUARANTEES.name: types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Гарантии нужны", callback_data="Гарантии нужны"),
                types.InlineKeyboardButton("Гарантии не нужны", callback_data="Гарантии не нужны"),
                types.InlineKeyboardButton("Пока не определился", callback_data="Пока не определился"),
            ),
            PartnerState.SET_EXPERIENCE.name: types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Можно без опыта", callback_data="Можно без опыта"),
                types.InlineKeyboardButton("До 50 завершенных дел", callback_data="До 50 завершенных дел"),
                types.InlineKeyboardButton("От 50 до 200 завершенных дел",
                                           callback_data="От 50 до 200 завершенных дел"),
                types.InlineKeyboardButton("От 200 до 1000 завершенных дел",
                                           callback_data="От 200 до 1000 завершенных дел"),
                types.InlineKeyboardButton("Более 1000 завершенных дел", callback_data="Более 1000 завершенных дел"),
            ),
        }
        self.bot.send_reply_message(text=state_messages[self.current_state.name],
                                    reply_markup=state_keyboard[self.current_state.name])