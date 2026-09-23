import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
SMTP_USER = os.getenv("EMAIL_SMTP_USER")
SMTP_PASSWORD = os.getenv("EMAIL_SMTP_PASSWORD")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
NOTIFY_TO = os.getenv("NOTIFY_EMAIL_TO")  # where lead notifications are sent; defaults to SMTP_USER


def send_email_notification(subject: str, body: str) -> bool:
    """Best-effort email notification. Returns False (and never raises) if SMTP
    isn't configured yet, so bookings/enquiries always succeed either way."""
    if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD):
        return False
    to_addr = NOTIFY_TO or SMTP_USER
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_addr
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [to_addr], msg.as_string())
        return True
    except Exception as e:
        print(f"[email notification failed] {e}")
        return False
