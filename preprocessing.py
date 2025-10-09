import email_injection
from email import policy
from email.parser import BytesParser
import re
import html
import unicodedata

def parse_email(raw_email):
    msg = BytesParser(policy=policy.default).parsebytes(raw_email)
    subject = msg['subject']
    sender = msg['from']
    
    # Extract body content
    body_part = msg.get_body(preferencelist=('plain', 'html'))
    body = body_part.get_content() if body_part else ""
    
    # Extract links
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
    
    # Check for attachments
    has_attachments = False
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                has_attachments = True
                break
    
    return {
        "from": sender, 
        "subject": subject, 
        "body": body,
        "links": links,
        "has_attachments": has_attachments
    }

def clean_text(text):
    text = html.unescape(text)
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text 

def preprocess_emails(username, password, folder="inbox"):
    M = email_injection.connect(username, password)
    if M is None: 
        return []
    
    raw_emails = email_injection.fetch_emails(M, folder)
    preprocessed_emails = []

    for raw_email in raw_emails:
        parsed_email = parse_email(raw_email)
        parsed_email['subject'] = clean_text(parsed_email['subject'])
        parsed_email['body'] = clean_text(parsed_email['body'])
        preprocessed_emails.append(parsed_email)
    
    M.logout()
    return preprocessed_emails
