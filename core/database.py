# core/database.py
"""
Database Connection Manager

This module establishes and manages a connection to the MongoDB database using pymongo.
It provides a function to obtain the database instance which can be used throughout the project.
"""

from pymongo import MongoClient
from config import settings
import certifi
import logging

logger = logging.getLogger(__name__)

def get_db():
    """
    Establish and return a connection to the MongoDB database.

    Returns:
        db: The MongoDB database instance.
    """
    try:
        client = MongoClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
        db = client['telegrambotdatabase']
        return db
    except Exception as e:
        logger.error("Failed to connect to MongoDB", exc_info=True)
        raise e
