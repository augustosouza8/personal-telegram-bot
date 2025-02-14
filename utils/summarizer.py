# utils/summarizer.py
"""
Conversation Summarizer Module

This module manages an updated summary (or "resume") of the conversation for each user.
Instead of keeping a full conversation history, we store only a summary that is updated
after every 3 new user messages.

Database Schema (in the "conversation_summaries" collection):
    - user_id: Unique identifier of the user.
    - summary: Current conversation summary text (max 300 words).
    - unsummarized_count: Count of new user messages since the last summary update.
    - buffer: Concatenated new interactions (with role labels) not yet incorporated into the summary.

Workflow:
    1. When a new message arrives, this module appends it to the buffer.
    2. For "User" messages, unsummarized_count is incremented.
    3. If unsummarized_count reaches 3, a prompt is constructed:
         "Please summarize the following conversation into a maximum of 300 words.
          Current summary: <existing summary>
          New interactions: <buffer>"
       The Groq LLM API is then called to produce an updated summary.
    4. The summary is updated in the database, unsummarized_count is reset to 0, and the buffer is cleared.
    5. The function returns the current (possibly updated) summary.
"""

import time
from core.database import get_db
from core.llm import get_llm_response

# Threshold for updating the summary (after every 3 user messages)
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

    Implementation Details:
        - If no summary exists for the user, create a new record.
        - Append the new message (prefixed with its role) to the buffer.
        - For "User" messages, increment the unsummarized_count.
        - If unsummarized_count >= UPDATE_THRESHOLD, construct a summarization prompt,
          call the LLM to update the summary, and reset the counter and buffer.
    """
    db = get_db()
    collection = db.conversation_summaries

    # Retrieve existing summary record; if none, create a new one.
    record = collection.find_one({"user_id": user_id})
    if not record:
        record = {
            "user_id": user_id,
            "summary": "",  # Initially empty summary.
            "unsummarized_count": 0,
            "buffer": ""
        }
        collection.insert_one(record)

    # Append the new message to the buffer with a role label.
    new_entry = f"{role}: {new_message}\n"
    updated_buffer = record.get("buffer", "") + new_entry

    # For user messages, increment the unsummarized counter.
    unsummarized_count = record.get("unsummarized_count", 0)
    if role == "User":
        unsummarized_count += 1

    # Prepare the update document.
    update_fields = {
        "buffer": updated_buffer,
        "unsummarized_count": unsummarized_count,
        "last_updated": time.time()
    }


    # If we've reached the update threshold for user messages, update the summary.
    if unsummarized_count >= UPDATE_THRESHOLD:
        print(f"The threshold count is {unsummarized_count}, thus the summary in being updated:\n")
        current_summary = record.get("summary", "")
        prompt = (

            f"You are tasked with maintaining a conversational context between a user and a bot. "
            f"Below you'll find: \n1. A current summary of their previous interactions.\n"
            f"2. The most recent exchanges between them.\n"
            f"Generate a new comprehensive summary that: \n"
            f"- Integrates key information from both the current summary and new interactions \n"
            f"- Preserves essential context needed for future exchanges \n"
            f"- Highlights any significant changes in topic or important decisions made \n"
            f"- Maintains chronological flow of important events/topics \n"
            f"- Uses clear, concise language \n"
            f"Maximum length: 300 words \n"
            f"Current Summary: {current_summary} \n"
            f"Recent Interactions: {updated_buffer} \n"
            f"Output only the new summary text, without any additional commentary or sections."
        )
        try:
            # Call the Groq LLM API to generate a new summary.
            new_summary = get_llm_response(prompt)
            # Update the summary and reset counter and buffer.
            update_fields["summary"] = new_summary
            update_fields["unsummarized_count"] = 0
            update_fields["buffer"] = ""
        except Exception as e:
            # In case of error, fallback to using the existing summary.
            new_summary = current_summary
        updated_summary = new_summary
    else:
        updated_summary = record.get("summary", "")
        print(f"The threshold count is {unsummarized_count}, thus the summary wasn't updated.")

    # Save the updated record.
    collection.update_one({"user_id": user_id}, {"$set": update_fields})
    return updated_summary
