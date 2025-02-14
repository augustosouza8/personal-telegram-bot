# handlers/notification.py
"""
Notification Handler Module

This module sends email notifications for events such as media requests or system errors.
"""

import logging
import smtplib
from email.mime.text import MIMEText
from config import settings

logger = logging.getLogger(__name__)

def send_email_alert(subject: str, message: str) -> None:
    """
    Send an email alert with the specified subject and message.

    Args:
        subject (str): Subject of the email.
        message (str): Message body containing details of the alert.
    """
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_SENDER
        msg['To'] = settings.EMAIL_SENDER

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info("Email alert sent: %s", subject)
    except Exception as e:
        logger.error("Failed to send email alert", exc_info=True)
