# handlers/message.py
"""
Message Handler Module (Updated for Conversation Summarization)

This module processes incoming messages with the following steps:
    1. Preprocesses the user's message.
    2. Checks for media requests and sends an email alert if needed.
    3. Updates the conversation summary using the summarizer module.
    4. Constructs a prompt that includes the base personality, current conversation summary,
       and the new user message.
    5. Calls the LLM integration module (Groq API) to generate a response.
    6. Updates the conversation summary with the bot's response.
    7. Returns the generated response.
"""

from config import personality
from core import llm
from handlers import notification
from utils import summarizer
import time


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
    Process an incoming user message:
        1. Preprocess the message.
        2. Check for media requests and send an alert if found.
        3. Update the conversation summary with the new user message.
        4. Construct a prompt using the base personality and current summary.
        5. Generate a response using the LLM.
        6. Update the conversation summary with the bot's response.
        7. Return the bot's response.

    Args:
        message_text (str): The incoming user message.
        user_id (int): The user's unique identifier.

    Returns:
        str: The generated response from the LLM.
    """
    # Step 1: Preprocess the message.
    processed_text = preprocess_message(message_text)

    # Step 2: Check for media request keywords.
    if check_media_request(processed_text):
        subject = "Media Request Detected"
        alert_message = f"User {user_id} requested media with message: {processed_text}"
        notification.send_email_alert(subject, alert_message)

    # Step 3: Update the conversation summary with the new user message.
    current_summary = summarizer.update_summary(user_id, processed_text, role="User")



    # Step 4: Construct the prompt for generating the bot's reply.
    prompt = (
        f"You are engaging in a playful, lighthearted flirting conversation with the user. Your responses should be:\n"
        f"- Authentic and natural, avoiding clichés\n"
        f"- Respectful and appropriate\n"
        f"- Responsive to the user's energy and engagement level\n"
        f"- Maintaining consistent personality traits\n"
        f"- Building upon shared interests and previous topics\n"
        f"\n"
        f"Previous Context Summary:\n"
        f"{current_summary}\n"
        f"\n"
        f"User\'s Latest Message:\n"
        f"{processed_text}\n"
        f"\n"
        f"Respond naturally to continue the conversation while:\n"
        f"- Acknowledging points from their latest message\n"
        f"- Referring to relevant details from previous exchanges when appropriate\n"
        f"- Maintaining a playful but respectful tone\n"
        f"- Including occasional questions to keep the conversation flowing\n"
        f"- Staying within appropriate boundaries\n"
        f"\n"
        f"Generate only your next response in a conversational tone, without any additional commentary or meta-discussion. Try to not give answers if more than 210 characters, just when it's totally necessary"
    )

    # Step 5: Generate the response using the Groq LLM.
    try:
        response = llm.get_llm_response(prompt)
    except Exception as e:
        subject = "LLM API Failure"
        error_message = f"Error generating response for user {user_id} with prompt: {prompt}\nError: {str(e)}"
        notification.send_email_alert(subject, error_message)
        raise e

    # Step 6: Update the conversation summary with the bot's response.
    summarizer.update_summary(user_id, response, role="Bot")
    print("Response sent to conversation summary.")

    # Step 7: Return the generated response.
    return response
