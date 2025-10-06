from imaplib import IMAP4

class EmailClient:
    def __init__(self):
        self.connection = None
        self.logged_in = False 
        self.selected_mailbox = None
        self.search_criteria = None 
        self.fetch_data = None 
        self.email_ids = []
    
    def connect(self, server: str, port: int = 993):
        self.connection = IMAP4(server, port)
        self.connection.starttls()
        print(f"connected to {server}: {port}")
    
    def login(self, username: str, password: str):
        if self.connection:
            self.connection.login(username, password)
            self.logged_in = True
            print("Logged in successfully")
        else:
            print("connection not established yet - call connect() first")

    def select_mailbox(self, mailbox: str = "INBOX"):
        if self.logged_in:
            self.connection.select(mailbox)
            self.selected_mailbox = mailbox
            print(f"Selected mailbox: {mailbox}")
        else:
            print("Not logged in - call login() first")
        
    def search_emails(self, criteria: str = "ALL"):
        if self.selected_mailbox:
            status, data = self.connection.search(None, criteria)
            if status == "OK":
                self.email_ids = data[0].split()
                self.search_criteria = criteria
                print(f"Found {len(self.email_ids)} emails matching criteria: {criteria}")
            else:
                print("Search failed")
        else:
            print("No mailbox selected - call select_mailbox() first")
    
    def fetch_email(self, email_id: bytes, data: str = "(RFC822)"):
        if email_id in self.email_ids:
            status, fetched_data = self.connection.fetch(email_id, data)
            if status == "OK":
                self.fetch_data = fetched_data
                print(f"Fetched email ID: {email_id.decode()}")
                return fetched_data
            else:
                print("Fetch failed")
        else:
            print("Email ID not found in the current search results")
