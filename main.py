import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime
import os

# Get your bot token from Render environment variable
BOT_TOKEN = os.getenv 8225680034:AAHaKFH71PbrakuD7bA1UbjYvwAzDs6muuE

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
            try:
                # Delete the message that broke the cooldown
                await update.message.delete()
                # Send a temporary warning message
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ Please wait {COOLDOWN_SECONDS} seconds before sending another message.",
                    reply_to_message_id=update.message.message_id
                )
            except Exception as e:
                print("Error handling cooldown:", e)
            return

    # Update last message time for this user
    last_message_time[chat_id][user_id] = now

# Create and run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Cooldown bot is running...")
app.run_polling()
