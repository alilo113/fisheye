import imaplib

def connect(username, password):
    try:
        M = imaplib.IMAP4_SSL("imap.gmail.com")
        M.login(username, password)
        return M
    except imaplib.IMAP4.error:
        print("LOGIN FAILED!")
        return None
    
def fetch_emails(M, folder="inbox"):
    M.select(folder)
    typ, data = M.search(None, 'ALL')
    mail_ids = data[0].split()
    emails = []
    for mail_id in mail_ids:
        typ, msg_data = M.fetch(mail_id, '(RFC822)')
        emails.append(msg_data[0][1])
    return emails
