# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

# Telegram Bot API token (obtained from BotFather)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Groq API key for LLM integration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# MongoDB connection URI
MONGODB_URI = os.getenv("MONGODB_URI")

# Email credentials for sending notifications.
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Default rate limit (number of messages allowed per hour)
DEFAULT_RATE_LIMIT_PER_HOUR = int(os.getenv("DEFAULT_RATE_LIMIT_PER_HOUR", 30))
