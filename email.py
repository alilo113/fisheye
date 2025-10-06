from imaplib import IMAP4

def resive_emails_from_mailbox(mail: IMAP4, mailbox: str = "INBOX") -> list:
    mail.select(mailbox)
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    emails = []
    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        emails.append(msg_data[0][1])
    return emails
