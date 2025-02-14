# config/personality.py
"""
Personality Configuration Module

This module defines the base personality for the Telegram bot and provides a structure for
storing user-specific personality adaptations based on conversation history.

Minimum information required:
    - Base personality traits (e.g., greeting, compliment, farewell)
    - A structure for adaptive personality traits (to be populated based on individual conversations)

You can modify the base personality and add more traits as needed.
"""

# Base personality traits for the bot (pre-set flirtatious style)
base_personality = {
    "greeting": "Your main role is to pretend that we are flirting.",
    "compliment": "You look absolutely stunning today.",
    "farewell": "Take care, and remember, I'm just a message away."
}

# Adaptive personality traits dictionary.
# This will be populated dynamically based on each user's conversation history.
adaptive_personality = {}

def update_adaptive_personality(user_id: int, conversation_history: list) -> str:
    """
    Update and return the adaptive personality for the given user based on conversation history.
    For demonstration, if the conversation has more than 3 user messages, we add an extra friendly sentence.

    Args:
        user_id (int): The user's unique identifier.
        conversation_history (list): List of conversation messages (dictionaries).

    Returns:
        str: The adaptive personality string to be appended to the base personality.
    """
    # Count how many messages are from the user.
    user_messages = [doc for doc in conversation_history if doc.get("message", "").startswith("User:")]
    if len(user_messages) > 3:
        adaptive_text = "I really enjoy our conversation and getting to know you better!"
    else:
        adaptive_text = ""
    # Store or update the adaptive personality for this user.
    adaptive_personality[user_id] = adaptive_text
    return adaptive_text
