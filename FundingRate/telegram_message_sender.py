import telegram
from credentials import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
telegram_bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_message(message):
    if not message:
        return
    try:
        telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        pass
