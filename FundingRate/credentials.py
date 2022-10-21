from os import getenv
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = getenv('BINANCE_SECRET_KEY')
TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = getenv('TELEGRAM_CHAT_ID')