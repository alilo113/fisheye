from imaplib import IMAP4, IMAP4_SSL

def email_ingestion(
    host: str,
    username: str,
    password: str,
    mailbox: str = "INBOX",
    port: int = 993,
    use_ssl: bool = True,
    search_criteria: str = 'ALL',
):
    if use_ssl:
        mail = IMAP4_SSL(host, port)
    else:
        mail = IMAP4(host, port)
    
    mail.login(username, password)
    mail.select(mailbox)
    result, data = mail.search(None, search_criteria)
    email_ids = data[0].split()
    
    emails = []

    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, '(RFC822)')
        if result == 'OK':
            emails.append(msg_data[0][1])
