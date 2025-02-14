# utils/rate_limiter.py
"""
Rate Limiter Module

This module implements a basic rate limiting mechanism to control the number of messages
a user can send within a given time frame. The default limit is configurable via the settings.
"""

import time
from config import settings

# Dictionary to track message timestamps for each user (in-memory storage).
user_message_timestamps = {}


def is_rate_limited(user_id: int) -> bool:
    """
    Check if a user has exceeded the rate limit.

    Args:
        user_id (int): Unique identifier for the user.

    Returns:
        bool: True if the user is rate limited, False otherwise.
    """
    current_time = time.time()
    # Retrieve or initialize the list of message timestamps for the user.
    timestamps = user_message_timestamps.get(user_id, [])

    # Filter timestamps to include only those from the last hour (3600 seconds).
    timestamps = [timestamp for timestamp in timestamps if current_time - timestamp < 3600]
    user_message_timestamps[user_id] = timestamps  # Update the stored timestamps

    print(f"This is the current user rate: {user_message_timestamps}")

    # If the user has already sent the maximum allowed messages, they are rate limited.
    if len(timestamps) >= settings.DEFAULT_RATE_LIMIT_PER_HOUR:
        return True

    # Otherwise, record the current message timestamp.
    timestamps.append(current_time)
    user_message_timestamps[user_id] = timestamps
    return False
