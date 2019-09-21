import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CREDENTIALS_PATH = os.environ['CREDENTIALS_PATH']