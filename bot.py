import os
from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token and group ID from .env
TOKEN = os.getenv('TELEGRAM_TOKEN')
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID'))

# Group rules (sent every 48h)
RULES_MESSAGE = """
📜 **Group Rules** 📜
1. Be respectful.
2. No spam.
3. Stay on topic.
"""

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("I'm your group manager bot!")

def delete_join_messages(update: Update, context: CallbackContext) -> None:
    """Delete 'user joined' messages."""
    if update.message.new_chat_members:
        update.message.delete()

def send_rules(context: CallbackContext) -> None:
    """Send rules every 48 hours."""
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text=RULES_MESSAGE, parse_mode='Markdown')

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, delete_join_messages))

    # Job queue (send rules every 48h)
    job_queue = updater.job_queue
    job_queue.run_repeating(send_rules, interval=172800, first=10)  # 48h in seconds

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()