import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

logger.info('Loading environment vars...')

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_API_ID = os.environ['TELEGRAM_API_ID']
TELEGRAM_API_HASH = os.environ['TELEGRAM_API_HASH']

CREDENTIALS = os.environ['CREDENTIALS']

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']

logger.info('Environment vars loaded!')