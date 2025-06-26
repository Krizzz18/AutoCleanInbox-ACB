import imaplib
import email
from email.header import decode_header

def fetch_emails(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    
    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()
    email_texts = []

    for num in mail_ids[-50:]:  # Last 50 emails
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode("utf-8", errors="ignore")
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                full_text = subject + " " + body
                email_texts.append(full_text)

    mail.logout()
    return email_texts
