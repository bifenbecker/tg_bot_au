import logging
import os
import settings
import uvicorn
from webhook import app
from dotenv import load_dotenv
from bot import BotFactory

load_dotenv()
logging.basicConfig(level=logging.DEBUG)


def production_run():
    bot = BotFactory.create_bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    bot.remove_webhook()

    # Set webhook
    bot.set_webhook(
        url=settings.WEBHOOK_URL_BASE + settings.WEBHOOK_URL_PATH,
        certificate=open(settings.WEBHOOK_SSL_CERT, 'r')
    )

    uvicorn.run(
        app,
        host=settings.WEBHOOK_LISTEN,
        port=settings.WEBHOOK_PORT,
        ssl_certfile=settings.WEBHOOK_SSL_CERT,
        ssl_keyfile=settings.WEBHOOK_SSL_PRIV
    )


def dev_run():
    bot = BotFactory.create_bot(token=settings.TELEGRAM_BOT_TOKEN)
    bot.run()


if __name__ == '__main__':
    environment = os.getenv('ENV')
    if environment == 'dev':
        dev_run()
    else:
        production_run()
