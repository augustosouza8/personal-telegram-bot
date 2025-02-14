# utils/memory.py
"""
Memory Module

This module manages conversation memory by storing and retrieving the full conversation history
for each user from MongoDB.

In this phase, all messages are stored indefinitely. Future iterations might include summarization
or context window management.
"""

from core.database import get_db
import time

def store_message(user_id: int, message: str) -> None:
    """
    Store a user's message in the conversation history.

    Args:
        user_id (int): Unique identifier for the user.
        message (str): The message text to store.
    """
    db = get_db()
    # Insert the message along with a timestamp into the 'conversations' collection.
    db.conversations.insert_one({
        "user_id": user_id,
        "message": message,
        "timestamp": time.time()
    })

def get_conversation(user_id: int) -> list:
    """
    Retrieve the full conversation history for a user.

    Args:
        user_id (int): Unique identifier for the user.

    Returns:
        list: List of message documents sorted by timestamp.
    """
    db = get_db()
    conversation = list(db.conversations.find({"user_id": user_id}).sort("timestamp", 1))
    return conversation
