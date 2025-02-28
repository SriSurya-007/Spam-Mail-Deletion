import imaplib
import email
import smtplib
import openpyxl
from email.header import decode_header
from email.message import EmailMessage
from datetime import datetime
import os
from collections import defaultdict

LOG_FILE_PATH = r'C:\Users\srisu_j75y5sd\OneDrive\Desktop\AutomationToDeleteEmail\AutomationToDeleteMail\logTime.txt'

EMAIL = "srisuryabondu01@gmail.com"
PASSWORD = "lcre jiyy mgcq kaok"  # Use an App Password if 2FA is enabled

ALERT_RECEIVER1 = "srisuryabondu01@gmail.com"  # Email to send alert
ALERT_RECEIVER2 = "venkata.bondu@gmail.com"  # Email to send alert

DELETE_CRITERIA = {  # Using a set for faster lookups
    "deletion", "congratulations", "(no subject)", "update", "application", "offer",
    "sale", "discount", "limited-time offer", "best price", "exclusive deal",
    "free trial", "coupon code", "promo", "promotional", "subscribe now",
    "save big", "act fast", "hurry, offer ends soon",
    "congratulations", "you won", "claim your prize", "urgent action required",
    "final notice", "unclaimed funds", "lottery winner", "dear customer",
    "bank account update", "suspicious login attempt", "confirm your details",
    "quick loan approval", "zero interest rate", "make money fast",
    "work from home and earn", "investment opportunity", "bitcoin giveaway",
    "no credit check required", "risk-free profit",
    "lose weight fast", "miracle cure", "get rid of wrinkles", "boost testosterone",
    "100% natural remedy", "doctor recommended",
    "update your preferences", "you are receiving this email because",
    "manage your subscription", "opt-out", "unsubscribe now", "reacted to a post", "limited time offer",
    "expiring soon", "linkedin", "threads", "truecaller", "Uber", "security alert", "you need to know", "promo",
    "are hiring"
}

TODAY_DATE = datetime.now().strftime("%Y-%m-%d")
EXCEL_FILE = f"deleted_emails_{TODAY_DATE}.xlsx"


def log_deleted_email(received_date, sender, subject, deleted_date):
    """Logs deleted emails into an Excel file."""
    try:
        wb = openpyxl.load_workbook(EXCEL_FILE)
        sheet = wb.active
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["Email Received Date", "Sender", "Subject", "Deleted Date"])  # Header row

    sheet.append([received_date, sender, subject, deleted_date])
    wb.save(EXCEL_FILE)


def send_alert_email(receiver, summary):
    """Sends an alert email with the log file and summary."""
    if not os.path.exists(EXCEL_FILE):
        print("Excel log file not found. Skipping alert email.")
        return

    msg = EmailMessage()
    msg["Subject"] = f"Spam Mail Deleted as of {datetime.today().strftime('%d-%m-%Y')}"
    msg["From"] = EMAIL
    msg["To"] = receiver
    msg.set_content(f"Attached is the log file containing details of deleted spam emails.\n\n{summary}")

    with open(EXCEL_FILE, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application",
                           subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=EXCEL_FILE)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        print(f"Alert email sent successfully to {receiver}")
    except Exception as e:
        print(f"Failed to send alert email: {e}")


def process_emails(mail):
    """Processes emails, deletes spam, logs them, and keeps count by sender."""
    mail.select("inbox")
    status, messages = mail.search(None, "FLAGGED")

    if status != "OK":
        print("No emails found.")
        return {}

    email_ids = messages[0].split()
    print(f"Total Emails Found: {len(email_ids)}")

    moved_count = 0
    sender_count = defaultdict(int)

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            continue

        for response_part in msg_data:
            if not isinstance(response_part, tuple):
                continue

            msg = email.message_from_bytes(response_part[1])
            subject = msg["Subject"]
            if subject:
                decoded_subject, encoding = decode_header(subject)[0]
                subject = decoded_subject.decode(encoding if encoding else "utf-8") if isinstance(decoded_subject, bytes) else decoded_subject
            else:
                subject = "No Subject"

            from_email = msg.get("From", "Unknown Sender")
            received_date_raw = msg["Date"]
            try:
                received_datetime = datetime.strptime(received_date_raw, "%a, %d %b %Y %H:%M:%S %z")
                received_date = received_datetime.strftime("%d-%m-%Y %H:%M:%S")
            except Exception:
                received_date = "Unknown"

            subject_lower = subject.lower()
            from_email_lower = from_email.lower()
            if any(term in subject_lower for term in DELETE_CRITERIA) or any(term in from_email_lower for term in DELETE_CRITERIA) or subject == "No Subject":
                print(f"Moving to Trash: {subject} from {from_email}")
                mail.copy(email_id, "[Gmail]/Trash")
                mail.store(email_id, "+FLAGS", "\\Deleted")
                log_deleted_email(received_date, from_email, subject, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                sender_count[from_email] += 1
                moved_count += 1

    if moved_count > 0:
        mail.expunge()
        print(f"Moved {moved_count} emails to Trash and logged them in {EXCEL_FILE}.")
    else:
        print("No matching emails found to move.")

    return sender_count


def main():
    """Main function to execute email deletion."""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)

        sender_count = process_emails(mail)
        if sender_count:
            summary = "The following are the number of mails deleted from each sender:\n" + "\n".join(f"{sender}: {count} mails" for sender, count in sender_count.items())
            send_alert_email(ALERT_RECEIVER1, summary)
            send_alert_email(ALERT_RECEIVER2, summary)

    except imaplib.IMAP4.error:
        print("Failed to login. Check your credentials.")
    finally:
        mail.logout()

if __name__ == "__main__":
    main()
