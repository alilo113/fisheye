from imaplib import IMAP4

def connect_to_email_server(server: str, username: str, password: str) -> IMAP4:
    """
    Connects to an IMAP email server and logs in with the provided credentials.

    Args:
        server (str): The IMAP server address.
        username (str): The username for the email account.
        password (str): The password for the email account.

    Returns:
        IMAP4: An instance of the IMAP4 class representing the connection.
    """
    mail = IMAP4(server)
    mail.login(username, password)
    return mail
