import telebot
import os
import messages
from telebot import types
from time import sleep
from datetime import datetime, timedelta
from dotenv import load_dotenv
from db.orm import Session
from db.models import User, StartRecord

load_dotenv()


def process():
    bot = telebot.TeleBot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    while True:
        with Session() as session:
            users = session.query(User).all()
            for user in users:
                last_record = session.query(StartRecord).filter(StartRecord.chat_id == user.telegram_id).order_by(
                    StartRecord.start_time.desc()).first()
                is_must_send_notification_per_one_day = int(
                    (last_record.start_time + timedelta(days=1)).timestamp()) < int(
                    datetime.utcnow().timestamp())
                is_must_send_notification_per_one_month = int(
                    (last_record.start_time + timedelta(days=30)).timestamp()) < int(
                    datetime.utcnow().timestamp())
                if is_must_send_notification_per_one_day:
                    bot.send_message(parse_mode='Markdown', chat_id=user.telegram_id,
                                     text=messages.NOTIFICATION_PER_ONE_DAY,
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
                    record = StartRecord(
                        chat_id=user.telegram_id,
                        username=user.username,
                    )
                    session.add(record)
                    session.commit()
                if is_must_send_notification_per_one_month:
                    bot.send_message(parse_mode='Markdown', chat_id=user.telegram_id,
                                     text=messages.NOTIFICATION_PER_ONE_MONTH,
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
                    record = StartRecord(
                        chat_id=user.telegram_id,
                        username=user.username,
                    )
                    session.add(record)
                    session.commit()
        sleep(60)


if __name__ == '__main__':
    process()
