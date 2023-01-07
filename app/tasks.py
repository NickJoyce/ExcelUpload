from project.celery import app
from .excel_file_handling.main import make_handling
import requests


import base64
from project.settings import BASE_DIR
from smtplib import SMTP_SSL
from email.message import EmailMessage
import os
from database.context_manager import db
from dotenv import load_dotenv

@app.task
def make_handling_task(user_id, file_base64, file_name):
    make_handling(user_id, file_base64, file_name)

@app.task
def regular_email_notification_task():
    # данные для подключения и входа на почту
    load_dotenv(f"{BASE_DIR}/.env")
    host = os.getenv('EMAIL_HOST')
    port = int(os.getenv('EMAIL_PORT'))
    user = os.getenv('EMAIL_HOST_USER')
    password = os.getenv('EMAIL_HOST_PASSWORD')

    # от кого
    from_name = "Regular"
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


@app.task
def regular_telegram_notification_task():
    load_dotenv(f"{BASE_DIR}/.env")
    url = os.getenv('TG_BOT_URL')
    token = os.getenv('TG_EXCEL_UPLOAD_BOT_TOKEN')
    telegram_id = "520704135"

    content = "Works!"

    requests.get(f"{url}{token}/sendMessage?chat_id={telegram_id}&text={content}")