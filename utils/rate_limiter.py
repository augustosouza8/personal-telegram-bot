# utils/rate_limiter.py
"""
Rate Limiter Module

This module implements a basic in-memory rate limiting mechanism to control the number of messages
a user can send within a given time frame.
"""

import time
import logging
from config import settings

logger = logging.getLogger(__name__)

# In-memory storage for user message timestamps.
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
    timestamps = user_message_timestamps.get(user_id, [])
    timestamps = [timestamp for timestamp in timestamps if current_time - timestamp < 3600]
    user_message_timestamps[user_id] = timestamps

    logger.debug("Current rate for user %s: %s", user_id, user_message_timestamps[user_id])

    if len(timestamps) >= settings.DEFAULT_RATE_LIMIT_PER_HOUR:
        return True

    timestamps.append(current_time)
    user_message_timestamps[user_id] = timestamps
    return False
