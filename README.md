# Personal Telegram Bot

A simple Telegram Bot powered by LLM that generates playful, flirtatious responses using the Groq API.

## Overview

This project uses a modular design with the following components:

- **config**: Configuration files and environment variable management
- **core**: Core integration logic for database and LLM (Groq API)
- **handlers**: Message and notification processing
- **utils**: Utility modules for rate limiting and conversation summarization

### Key Features

- **State Management**: Uses conversation summarization instead of full history storage
- **Rate Limiting**: In-memory rate limiting for message processing
- **Notification System**: Email alerts for media requests and errors
- **Logging**: Comprehensive logging system for debugging and operations

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/personal-telegram-bot.git
cd personal-telegram-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_uri
EMAIL_SENDER=your_email
EMAIL_PASSWORD=your_email_password
DEFAULT_RATE_LIMIT_PER_HOUR=30  # Optional, defaults to 30
```

## Running the Bot

Start the bot with:
```bash
python main.py
```

## Project Structure

```
personal-telegram-bot/
├── README.md
├── LICENSE
├── main.py
├── requirements.txt
├── config/
│   └── settings.py
├── core/
│   ├── database.py
│   └── llm.py
├── handlers/
│   ├── message.py
│   └── notification.py
└── utils/
    ├── rate_limiter.py
    └── summarizer.py
```

## Architecture Notes

- **Conversation Management**: Uses summarization instead of full conversation storage for efficient memory usage
- **Rate Limiting**: Implements in-memory rate limiting, sufficient for current usage
- **Removed Components**:
  - Personality module (settings were not actively used)
  - Full conversation memory module (replaced with summarization)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request