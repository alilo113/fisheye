import email_injection
from email import policy
from email.parser import BytesParser

def parse_email(raw_email):
    msg = BytesParser(policy=policy.default).parsebytes(raw_email)
    subject = msg['subject']
    sender = msg['from']
    body = msg.get_body(preferencelist=('plain', 'html')).get_content()
    return {"from": sender, "subject": subject, "body": body}
