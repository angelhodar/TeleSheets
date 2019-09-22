import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CREDENTIALS_PATH = os.environ['CREDENTIALS_PATH']

try:
    f = open(CREDENTIALS_PATH)
    f.close()
except FileNotFoundError:
    print('Credentials file path is not valid')

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']