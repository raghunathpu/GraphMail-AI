import imaplib
import email
from email.header import decode_header


def fetch_imap_emails(username, password, imap_server="imap.gmail.com"):
    print("Connecting to Gmail...")
    mail = imaplib.IMAP4_SSL(imap_server)

    print("Logging in...")
    mail.login(username, password)

    print("Opening inbox...")
    status, count = mail.select("INBOX")
    
    status, messages = mail.search(None, "ALL")
   
    email_ids = messages[0].split()[-10:]
    print("Email IDs found:", len(email_ids))

    emails = []

    print("Reading emails...")

    for num in email_ids:
        status, msg_data = mail.fetch(num, "(RFC822)")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg.get("Subject"))[0]

        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        emails.append(
            {
                "id": num.decode(),
                "from": msg.get("From"),
                "subject": subject,
                "body": extract_email_body(msg),
            }
        )

    mail.logout()

    print("Emails loaded:", len(emails))

    return emails


def extract_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if (
                content_type == "text/plain"
                and "attachment" not in content_disposition
            ):
                charset = part.get_content_charset() or "utf-8"

                return part.get_payload(decode=True).decode(
                    charset,
                    errors="replace"
                )

    else:
        charset = msg.get_content_charset() or "utf-8"

        return msg.get_payload(decode=True).decode(
            charset,
            errors="replace"
        )

    return ""
