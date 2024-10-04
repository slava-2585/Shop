import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML

from sqlalchemy.testing.suite.test_reflection import users

from config import settings, Settings


# username = settings.USERNAME
# password = settings.PASSWORD
# host = settings.HOST

# from_addr = os.getenv('FROM_ADDR')
# #port: int = int(os.getenv('PORT'))
# to_addr = 'slava-2585@yandex.ru'
# text_msg = 'Vsem privet'
# subject = "Test"


def send_email(to_addr, text_msg, subject):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = settings.FROM_ADR
    msg['To'] = to_addr
    # user: str =settings.USERNAME
    # pas: str = settings.PASSWORD
    msg.attach(MIMEText(text_msg, 'plain'))
    server = smtplib.SMTP(settings.HOST)
    server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()
    server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
    server.send_message(msg)
    server.quit()


