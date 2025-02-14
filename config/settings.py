# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from the .env file for local development.
# This is a best practice to keep sensitive credentials (e.g., API keys) out of your source code.
load_dotenv()

# Telegram Bot API token (obtained from BotFather)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Groq API key for LLM integration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# MongoDB connection URI
MONGODB_URI = os.getenv("MONGODB_URI")

# Email credentials for sending notifications (used for media request alerts and error notifications)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Default rate limit (number of messages allowed per hour)
# This is configurable via an environment variable, with a fallback default of 30.
DEFAULT_RATE_LIMIT_PER_HOUR = int(os.getenv("DEFAULT_RATE_LIMIT_PER_HOUR", 30))
