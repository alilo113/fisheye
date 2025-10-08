from email import message_from_bytes
import imaplib
import dns.resolver
import spf
import dkim
import tldextract
import preprocessing

def reading_sender_info(email_message):
    preprocessing.parse_email(email_message)
    sender = email_message["from"]
    return f"This message is from {sender}"
