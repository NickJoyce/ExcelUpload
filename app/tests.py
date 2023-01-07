import base64
from project.settings import BASE_DIR
from smtplib import SMTP_SSL
from email.message import EmailMessage
import os
from database.context_manager import db
from dotenv import load_dotenv

# данные для подключения и входа на почту

host = "mail.nic.ru"
port = 465
user = "admin@zvwb.ru"
password = "xN10zeq2"

# от кого
from_name = "Test"
from_email = user

msg = EmailMessage()
msg['subject'] = "---"
msg['from'] = f"{from_name} <{from_email}>"
msg.set_content("---")
msg['To'] = "actan-spb@mail.ru"

# отправка сообщений получателям
with SMTP_SSL(host, port) as smtp:
    smtp.ehlo()
    smtp.login(user, password)
    smtp.send_message(msg)



