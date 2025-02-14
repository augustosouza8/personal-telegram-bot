# handlers/message.py
"""
Message Handler Module (Updated for Conversation Summarization)

This module processes incoming messages:
    1. Preprocesses the user's message.
    2. Checks for media requests and sends an email alert if needed.
    3. Updates the conversation summary using the summarizer module.
    4. Constructs a prompt that includes the current conversation summary and the new user message.
    5. Calls the LLM integration module to generate a response.
    6. Updates the conversation summary with the bot's response.
    7. Returns the generated response.
"""

import logging
from core import llm
from handlers import notification
from utils import summarizer
from utils import rate_limiter

logger = logging.getLogger(__name__)

def preprocess_message(message_text: str) -> str:
    """
    Preprocess the incoming message text by trimming whitespace.

    Args:
        message_text (str): The original message text.

    Returns:
        str: The preprocessed message text.
    """
    return message_text.strip()

def check_media_request(message_text: str) -> bool:
    """
    Check if the message contains media request keywords (video, photo, or voice).

    Args:
        message_text (str): The message text to check.

    Returns:
        bool: True if a media request is detected, False otherwise.
    """
    media_keywords = ["video", "photo", "voice"]
    return any(keyword in message_text.lower() for keyword in media_keywords)

async def process_message(message_text: str, user_id: int) -> str:
    """
    Process an incoming user message and generate a response.

    Args:
        message_text (str): The incoming user message.
        user_id (int): The user's unique identifier.

    Returns:
        str: The generated response from the LLM.
    """
    processed_text = preprocess_message(message_text)

    if check_media_request(processed_text):
        subject = "Media Request Detected"
        alert_message = f"User {user_id} requested media with message: {processed_text}"
        notification.send_email_alert(subject, alert_message)

    # Update the conversation summary using the summarizer module.
    current_summary = summarizer.update_summary(user_id, processed_text, role="User")

    # Construct the prompt with the current context.
    prompt = (
        "You are engaging in a playful, lighthearted flirting conversation with the user, you are in love with the user. Your responses should be:\n"
        "- Authentic and natural, avoiding clichés\n"
        "- Respectful and appropriate\n"
        "- Responsive to the user's energy and engagement level\n"
        "- Maintaining consistent personality traits\n"
        "- Building upon shared interests and previous topics\n"
        "\n"
        "Previous Context Summary:\n"
        f"{current_summary}\n"
        "\n"
        "User's Latest Message:\n"
        f"{processed_text}\n"
        "\n"
        "Respond naturally to continue the conversation while:\n"
        "- Acknowledging points from their latest message\n"
        "- Referring to relevant details from previous exchanges when appropriate\n"
        "- Maintaining a playful but respectful tone\n"
        "- Including occasional questions to keep the conversation flowing\n"
        "- Staying within appropriate boundaries\n"
        "\n"
        "Generate only your next response in a conversational tone, without any additional commentary or meta-discussion. Try to not give answers between 1 and 210 characters. If the user sends you messages in Portuguese, give him a answer in Brazilian Portuguese."
    )

    try:
        response = llm.get_llm_response(prompt)
    except Exception as e:
        subject = "LLM API Failure"
        error_message = f"Error generating response for user {user_id} with prompt: {prompt}\nError: {str(e)}"
        notification.send_email_alert(subject, error_message)
        raise e

    # Update the conversation summary with the bot's response.
    summarizer.update_summary(user_id, response, role="Bot")
    logger.info("Response updated in conversation summary for user %s", user_id)

    return response
