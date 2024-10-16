import smtplib

from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML


from config import settings


async def send_email(to_addr, text_msg, subject):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = settings.FROM_ADR
    msg["To"] = to_addr
    # user: str =settings.USERNAME
    # pas: str = settings.PASSWORD
    msg.attach(MIMEText(text_msg, "plain"))
    server = smtplib.SMTP(settings.HOST)
    # server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()
    server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
    server.send_message(msg)
    server.quit()


def convert_tuple(lst):
    res: str = "Товар | Кол-во | Стоимость \n"
    for item in lst:
        s = " | ".join(map(str, item))
        s = s + "\n"
        res += s
    return res
