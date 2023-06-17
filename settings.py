import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent  # Edit if file move to another dir
PROJECT_DIR = os.path.basename(BASE_DIR)

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PORT = os.getenv('WEBHOOK_PORT')  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = os.getenv('WEBHOOK_LISTEN')  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = os.getenv('WEBHOOK_SSL_CERT')  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = os.getenv('WEBHOOK_SSL_PRIV')  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(TELEGRAM_BOT_TOKEN)


