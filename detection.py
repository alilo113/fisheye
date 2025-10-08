from email import message_from_bytes
import imaplib
import dns.resolver
import spf
import dkim
import tldextract
import preprocessing

def reading_sender_info(email_message):
    m = message_from_bytes(email_message)
    sender = m["From"]
    return f'This message is from {sender}'
