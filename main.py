import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
import os

BOT_TOKEN = os.getenv("8225680034:AAFY9EPDLfTh2em06b90G6UaElDtlYVoHT8")

last_message_time = {}
cooldown_seconds = 5  # cooldown between users

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_message_time
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    now = datetime.now()

    if chat_id not in last_message_time:
        last_message_time[chat_id] = {}

    # Find the most recent message time in this chat
    all_times = [t for t in last_message_time[chat_id].values()]
    if all_times:
        last_sent = max(all_times)
        if (now - last_sent).total_seconds() < cooldown_seconds:
            try:
                await update.message.delete()
            except:
                pass
            return

    last_message_time[chat_id][user_id] = now

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
