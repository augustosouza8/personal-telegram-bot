# main.py
"""
Main entry point for the Telegram Bot application.

This script initializes the bot, registers command and text message handlers, and starts the bot.
It now integrates the LLM-powered response generation and conversation history management.
"""

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import settings, personality
from handlers import message as message_handler
from utils import rate_limiter

# Configure logging to assist with debugging and runtime information.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for the /start command.

    Sends a welcome message using the bot's pre-set personality.
    """
    # Retrieve the greeting from the base personality settings.
    greeting = personality.base_personality.get("greeting", "Hello!")
    await update.message.reply_text(greeting)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming text messages from users.

    Steps:
    1. Checks if the user is within the rate limit.
    2. Processes the user's message using the updated message handler.
    3. Sends the LLM-generated response back to the user.
    """
    user_id = update.message.from_user.id
    if rate_limiter.is_rate_limited(user_id):
        # If the user is rate-limited, simply do not process further.
        return

    user_message = update.message.text
    # Process the message; pass both the message and the user ID for context.
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
    # Initialize the bot application using the token from our settings.
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Register the /start command handler.
    app.add_handler(CommandHandler("start", start))

    # Register a handler for all text messages (ignoring commands).
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Start the bot using long polling.
    app.run_polling()


if __name__ == "__main__":
    main()
