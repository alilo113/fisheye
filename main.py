import argparse
import json
from email_injection import connect, fetch_emails
from detection import analyze_email_safety

def main():
    parser = argparse.ArgumentParser(description='FishEye Phishing Detector')
    parser.add_argument('--email', help='Path to email file')
    parser.add_argument('--user', help='Email username for IMAP')
    parser.add_argument('--pass', help='Email password for IMAP')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    args = parser.parse_args()

    if args.email:
        with open(args.email, 'rb') as f:
            raw_email = f.read()
            result = analyze_email_safety(raw_email)
            output_result(result, args.json)
    
    elif args.user and args.pass:
        M = connect(args.user, args.pass)
        if M:
            emails = fetch_emails(M)
            print(f"Analyzing {len(emails)} emails...")
            for i, raw_email in enumerate(emails[:5]):
                result = analyze_email_safety(raw_email)
                print(f"\nEmail #{i+1}:")
                output_result(result, args.json)
            M.logout()
    else:
        parser.print_help()

def output_result(result, as_json=False):
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Result: {result['result']}")
        print(f"Score: {result['score']}/100")
        print("Reasons:")
        for reason in result['reasons']:
            print(f"  - {reason}")

if __name__ == "__main__":
    main()
