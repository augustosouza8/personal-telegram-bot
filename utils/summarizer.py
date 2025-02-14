# utils/summarizer.py
"""
Conversation Summarizer Module

This module manages a summarized conversation context for each user.
Instead of storing the full conversation history, a summary is maintained which is updated
after every 3 new user messages. This approach reduces storage overhead and retains essential
context for generating responses.

Database Schema (collection: "conversation_summaries"):
    - user_id: Unique identifier for the user.
    - summary: Current conversation summary text.
    - unsummarized_count: Number of new user messages since the last summary update.
    - buffer: Concatenated new interactions not yet incorporated into the summary.
"""

import time
import logging
from core.database import get_db
from core.llm import get_llm_response

logger = logging.getLogger(__name__)

# Threshold for updating the summary.
UPDATE_THRESHOLD = 3

def update_summary(user_id: int, new_message: str, role: str = "User") -> str:
    """
    Update the conversation summary for a user with a new interaction.

    Args:
        user_id (int): Unique identifier for the user.
        new_message (str): The new message text to incorporate.
        role (str): Role of the sender ("User" or "Bot").

    Returns:
        str: The current conversation summary after potential update.
    """
    db = get_db()
    collection = db.conversation_summaries

    # Retrieve existing summary record; if none, create a new one.
    record = collection.find_one({"user_id": user_id})
    if not record:
        record = {
            "user_id": user_id,
            "summary": "",
            "unsummarized_count": 0,
            "buffer": ""
        }
        collection.insert_one(record)

    # Append the new message to the buffer with a role label.
    new_entry = f"{role}: {new_message}\n"
    updated_buffer = record.get("buffer", "") + new_entry

    # Increment unsummarized count for user messages.
    unsummarized_count = record.get("unsummarized_count", 0)
    if role == "User":
        unsummarized_count += 1

    update_fields = {
        "buffer": updated_buffer,
        "unsummarized_count": unsummarized_count,
        "last_updated": time.time()
    }

    # Update summary if the unsummarized count reaches the threshold.
    if unsummarized_count >= UPDATE_THRESHOLD:
        logger.info("Threshold reached for user %s (%s messages). Updating summary.", user_id, unsummarized_count)
        current_summary = record.get("summary", "")
        prompt = (
            "You are tasked with maintaining a conversational context between a user and a bot. "
            "Below you'll find:\n1. A current summary of their previous interactions.\n"
            "2. The most recent exchanges between them.\n"
            "Generate a new comprehensive summary that:\n"
            "- Integrates key information from both the current summary and new interactions\n"
            "- Preserves essential context for future exchanges\n"
            "- Highlights significant changes in topic or important decisions made\n"
            "- Maintains chronological flow of key events/topics\n"
            "- Uses clear, concise language\n"
            "Maximum length: 300 words\n"
            f"Current Summary: {current_summary}\n"
            f"Recent Interactions: {updated_buffer}\n"
            "Output only the new summary text, without any additional commentary."
        )
        try:
            new_summary = get_llm_response(prompt)
            update_fields["summary"] = new_summary
            update_fields["unsummarized_count"] = 0
            update_fields["buffer"] = ""
            updated_summary = new_summary
            logger.info("Summary updated for user %s.", user_id)
        except Exception as e:
            updated_summary = current_summary
            logger.error("Failed to update summary for user %s. Keeping existing summary.", user_id, exc_info=True)
    else:
        updated_summary = record.get("summary", "")
        logger.info("Summary not updated for user %s. Unsummarized count: %s", user_id, unsummarized_count)

    collection.update_one({"user_id": user_id}, {"$set": update_fields})
    return updated_summary
