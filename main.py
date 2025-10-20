import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime

BOT_TOKEN = "8225680034:AAHaKFH71PbrakuD7bA1UbjYvwAzDs6muuE"

# Cooldown settings
last_message_time = {}
COOLDOWN_SECONDS = 5  # seconds between messages

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
        if (now - last_sent).total_seconds() < COOLDOWN_SECONDS:
            # Just ignore messages during cooldown (no delete, no warning)
            return

    # Update last message time for this user
    last_message_time[chat_id][user_id] = now

# Create and run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Cooldown bot is running...")
# Fixed Conflict issue
app.run_polling(drop_pending_updates=True)
