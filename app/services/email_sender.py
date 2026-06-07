import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import GMAIL_USER, GMAIL_APP_PASSWORD

def send_gmail_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: str | None = None,
    app_password: str | None = None
):
    """
    Sends an email using Gmail SMTP SSL (port 465).
    Falls back to env config variables if parameters are not explicitly provided.
    """
    sender = from_email or GMAIL_USER
    password = app_password or GMAIL_APP_PASSWORD

    if not sender or not password:
        raise ValueError(
            "Gmail sender email or App Password is not configured. "
            "Please configure GMAIL_USER and GMAIL_APP_PASSWORD in your .env, "
            "or provide them in the settings."
        )

    # Set up email message
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Send email via Gmail SMTP SSL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
