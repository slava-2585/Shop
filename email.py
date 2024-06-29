import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML

import smtplib

from config import settings

username = settings.USERNAME
password = settings.PASSWORD
host = settings.HOST

from_addr = os.getenv('FROM_ADDR')
port: int = int(os.getenv('PORT'))
to_addr = 'Nikiforov.vyacheslav@sigma.spb.ru'
text_msg = 'Vsem privet'
subject = "Test"


def send_email(msg, username, password, host):
    # msg = MIMEMultipart()
    # msg['Subject'] = subject
    # msg['From'] = from_addr
    # msg['To'] = to_addr
    # msg.attach(MIMEText(text_msg, 'plain'))
    server = smtplib.SMTP(host)
    #server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()


