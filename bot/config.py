import os
import json
from telegram.ext import Updater
from loguru import logger


logger.add('logs/debug.log', level="WARNING", rotation="50 MB", compression='zip',
           enqueue=True, backtrace=True, diagnose=True)

# load_dotenv()

TOKEN = os.getenv('TOKEN')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_DB = os.getenv('POSTGRES_DB')

PHOTO_PATH = os.getenv('PHOTO_PATH')

with open('utils/text_settings.json', 'r', encoding='utf-8') as file:
    SETTINGS = json.loads(file.read())

updater = Updater(TOKEN)

END_CONDITION = {}
