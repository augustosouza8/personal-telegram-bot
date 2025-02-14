# handlers/notification.py
"""
Notification Handler Module

This module is responsible for sending email notifications for events such as media requests
or system errors. The notifications include an alert and the message triggering the alert.
"""

import smtplib
from email.mime.text import MIMEText
from config import settings


def send_email_alert(subject: str, message: str) -> None:
    """
    Send an email alert with the specified subject and message.

    Args:
        subject (str): Subject of the email.
        message (str): Message body containing details of the alert.

    Note:
        This function uses SMTP with SSL. Adjust the SMTP server settings as needed.
    """
    try:
        # Create a MIMEText object with the alert message.
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_SENDER
        # For demonstration, we send the alert to the same email (EMAIL_SENDER).
        msg['To'] = settings.EMAIL_SENDER

        # Establish a secure connection with the SMTP server (using Gmail's SMTP server as an example).
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Log in using the email credentials from settings.
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            # Send the email message.
            server.send_message(msg)
    except Exception as e:
        # In case of failure, print the error message.
        print(f"Failed to send email alert: {e}")
