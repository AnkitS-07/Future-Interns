from dotenv import load_dotenv
load_dotenv()

from telegram.ext import Updater, MessageHandler, Filters
from dialogflow_utils import detect_intent
from gpt_fallback import gpt_response
from sentiment import get_sentiment
from escalation import escalate_to_human
from chat_logger import log_chat
import os

def handle_message(update, context):
    user_text = update.message.text
    user_name = update.message.from_user.username or "telegram_user"

    result = detect_intent(user_text)

    if result.intent.is_fallback:
        response = gpt_response(user_text)
    else:
        response = result.fulfillment_text

    sentiment = get_sentiment(user_text)
    if sentiment == "angry":
        response = escalate_to_human(user_text)

    log_chat(user_name, user_text, response)
    update.message.reply_text(response)

updater = Updater(os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

print("🤖 Telegram bot is running...")
updater.start_polling()
updater.idle()
