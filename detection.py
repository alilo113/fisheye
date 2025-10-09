from email import message_from_bytes
import imaplib
import dns.resolver
import spf
import dkim
import tldextract
import preprocessing
from detection_engine import PhishingDetector

def analyze_email_safety(raw_email):
    """Analyze email using the detection engine"""
    parsed_email = preprocessing.parse_email(raw_email)
    detector = PhishingDetector()
    return detector.analyze_email(parsed_email)

def reading_sender_info(email_message):
    preprocessing.parse_email(email_message)
    sender = email_message["from"]
    return f"This message is from {sender}"
