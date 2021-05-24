import smtplib
import ssl
from email.mime.text import MIMEText

from settings import SSL_PORT, SMTP_SERVER, SENDER_EMAIL, SENDER_PASSWORD


class EmailSender:

    @classmethod
    def send(cls, html, subject, receiver_email):
        msg = MIMEText(html, 'html')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
