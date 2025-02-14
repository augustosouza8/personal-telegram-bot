# core/database.py
"""
Database Connection Manager

This module establishes and manages a connection to the MongoDB database using pymongo.
It provides a function to obtain the database instance which can be used throughout the project.
"""

from pymongo import MongoClient
from config import settings
import certifi  # Import certifi to get the path to the trusted certificate bundle

def get_db():
    """
    Establish and return a connection to the MongoDB database.

    Returns:
        db: The MongoDB database instance.
    """
    # Use the certificate authority bundle provided by certifi for SSL verification.
    client = MongoClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
    # For demonstration, we assume the database name is 'telegram_bot'.
    db = client['telegrambotdatabase']
    return db
