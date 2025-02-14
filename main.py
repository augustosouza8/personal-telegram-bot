# main.py
"""
Main entry point for the Telegram Bot application.

This script initializes the bot, registers command and text message handlers, and starts the bot.
It integrates the LLM-powered response generation and conversation summary management.
"""

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import settings
from handlers import message as message_handler
from utils import rate_limiter

# Configure logging for the application.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for the /start command.

    Sends a welcome message to the user.
    """
    greeting = "[en] So great to see you here! How can I make you smile today? Let’s begin our love story.\n [pt] Que ótimo ter você por aqui! Sou muuuuito melhor do que o bate-papo da Oul, está duvidando? Então bora começar a nossa história de amor!"

    await update.message.reply_text(greeting)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming text messages from users.

    Steps:
    1. Checks if the user is within the rate limit.
    2. Processes the user's message using the message handler.
    3. Sends the LLM-generated response back to the user.
    """
    user_id = update.message.from_user.id
    if rate_limiter.is_rate_limited(user_id):
        return

    user_message = update.message.text
    response = await message_handler.process_message(user_message, user_id)
    await update.message.reply_text(response)

def main():
    """
    Main function to set up and run the Telegram bot.

    Steps:
    1. Initialize the bot with the API token.
    2. Register command and text message handlers.
    3. Start polling for incoming updates.
    """
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
