import base64
from smtplib import SMTP_SSL
from project.settings.base import BASE_DIR
from dotenv import load_dotenv
from email.message import EmailMessage
import os
from database.context_manager import db






def send_email_notification(username, first_name, last_name, file_base64, file_name, errors):
    with db() as cursor:
        file = base64.b64decode(file_base64)
        load_dotenv(f"{BASE_DIR}/.env")
        # получаем name, email активных получателей уведомлений, если у email есть значение
        cursor.execute("""SELECT name, email FROM app_notificationrecipients 
                                  WHERE is_active=%s AND email IS NOT NULL""", (True,))
        notification_recipients = cursor.fetchall()

        # данные для подключения и входа на почту
        host = os.getenv('EMAIL_HOST')
        port = int(os.getenv('EMAIL_PORT'))
        user = os.getenv('EMAIL_HOST_USER')
        password = os.getenv('EMAIL_HOST_PASSWORD')

        # от кого
        from_name = "ExcelUpload"
        from_email = user

        # тема и контент письма
        content = ""
        subject = f"[ {username} ({first_name} {last_name}) ]"
        if errors:
            # тема письма
            subject = "[FAIL] " + subject + " заказы из файла не загружены"
            # текст письма
            content += "Заказы из файла не загружены. Произошли следующие ошибки:\n"
            for error in errors:
                content += "- " + error + '\n'
        else:
            subject = "[ OK ] " + subject + " заказы из файла успешно загружены"
            content += "Все отлично! заказы загружены"


        # формируем список сообщений
        msgs = []
        for name, email in notification_recipients:
            msg = EmailMessage()
            msg['subject'] = subject
            msg['from'] = f"{from_name} <{from_email}>"
            msg.set_content(content)
            msg.add_attachment(file, maintype='application', subtype='octet-stream', filename=file_name)
            msg['To'] = email
            msgs.append(msg)

        # отправка сообщений получателям
        with SMTP_SSL(host, port) as smtp:
            smtp.ehlo()
            smtp.login(user, password)

            for msg in msgs:
                smtp.send_message(msg)




if __name__ == "__main__":
    ...
