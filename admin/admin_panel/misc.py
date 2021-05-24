import smtplib
import ssl
from email.mime.text import MIMEText

from django.conf import settings


class EmailSender:

    @classmethod
    def send(cls, html, subject, receiver_email):
        msg = MIMEText(html, 'html')
        msg['Subject'] = subject
        msg['From'] = settings.SENDER_EMAIL
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SSL_PORT, context=context) as server:
            server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
            server.sendmail(settings.SENDER_EMAIL, receiver_email, msg.as_string())
