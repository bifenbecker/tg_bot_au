import telebot
import fastapi
import settings
from bot import BotFactory

app = fastapi.FastAPI(docs_url=None, redoc_url=None)


@app.post(f'/{settings.TELEGRAM_BOT_TOKEN}/')
def process_webhook(update: dict):
    """
    Process webhook calls
    """
    if update:
        update = telebot.types.Update.de_json(update)
        bot = BotFactory.create_bot(token=settings.TELEGRAM_BOT_TOKEN)
        bot.process_new_updates([update])
    else:
        return
