import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


# Initializes the logger
logger.add("logs/log.log", level="DEBUG", format="{time:D/M/YYYY - HH:mm:ss} | {level} | {module}:{function}:{line} | {message}")

logger.info('Loading environment vars...')

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_API_ID = os.environ['TELEGRAM_API_ID']
TELEGRAM_API_HASH = os.environ['TELEGRAM_API_HASH']

CREDENTIALS_PATH = os.environ['CREDENTIALS_PATH']

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']

logger.info('Environment vars loaded!')