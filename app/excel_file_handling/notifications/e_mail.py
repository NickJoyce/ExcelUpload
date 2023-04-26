import base64
from smtplib import SMTP_SSL
from project.settings.base import BASE_DIR
from dotenv import load_dotenv
from email.message import EmailMessage
import os
from database.queries import get_email_notification_recipients


class EmailNotification():
    def __init__(self):
        self.host = os.getenv('EMAIL_HOST')
        self.port = int(os.getenv('EMAIL_PORT'))
        self.user = os.getenv('EMAIL_HOST_USER')
        self.password = os.getenv('EMAIL_HOST_PASSWORD')
        self.from_name = "ExcelUpload"
        self.from_email = self.user

    def send(self, recipients: list[tuple], subject, content, file=None, filename=None):
        """recipients - tuple содержит 2 элемента: имя и email получателя"""
        messages = []
        for name, email in recipients:
            msg = EmailMessage()
            msg['subject'] = subject
            msg['from'] = f"{self.from_name} <{self.from_email}>"
            msg.set_content(content)
            if file and filename:
                msg.add_attachment(file, maintype='application', subtype='octet-stream', filename=filename)
            msg['To'] = email
            messages.append(msg)
        self.send_messages(messages)


    def send_messages(self, messages):
        with SMTP_SSL(self.host, self.port) as smtp:
            smtp.ehlo()
            smtp.login(self.user, self.password)

            for message in messages:
                smtp.send_message(message)


    def supply_order_created_success(self, username, first_name, last_name):
        recipients = get_email_notification_recipients()
        subject = f"[NEW ORDER] {username} ({first_name}, {last_name})"
        content = ""
        self.send(recipients=recipients, subject=subject, content=content)




    def supply_order_sucessfully_created(self, username, first_name, last_name, sales_channel, comment,
                                         recipient_address,recipient_full_name, recipient_phone):
        recipients = get_email_notification_recipients()
        subject = f"[NEW ORDER] {username} ({first_name}, {last_name})"
        content = f"Создан новый заказ.\n\n" \
                  f"Данные заказа:\n" \
                  f"Пользователь: {username} ({first_name} {last_name})\n" \
                  f"Канал продаж: {sales_channel}\n" \
                  f"Адрес: {recipient_address}\n" \
                  f"ФИО: {recipient_full_name}\n" \
                  f"Телефон: {recipient_phone}\n" \
                  f"Комментарий: {comment}"
        self.send(recipients=recipients, subject=subject, content=content)


    def counterparty_id_is_not_exist(self, username, first_name, last_name, sales_channel, comment, recipient_address,
                                                       recipient_full_name, recipient_phone, counterparty_id):
        recipients = get_email_notification_recipients()
        subject = f"[COUNTERPARTY DOES NOT EXIST] {username} ({first_name}, {last_name})"
        content = f"Не удалось загрузить заказ в МойСклад.\n\nКонтрагента с id={counterparty_id} не существует.\n\n" \
                  f"Данные заказа:\n" \
                  f"Пользователь: {username} ({first_name} {last_name})\n" \
                  f"Канал продаж: {sales_channel}\n" \
                  f"Адрес: {recipient_address}\n" \
                  f"ФИО: {recipient_full_name}\n" \
                  f"Телефон: {recipient_phone}\n" \
                  f"Комментарий: {comment}"
        self.send(recipients=recipients, subject=subject, content=content)

    def general_error(self, username, first_name, last_name, error):
        recipients = get_email_notification_recipients()
        subject = f"[APP ERROR] {username} ({first_name} {last_name})"
        content = f"{error}"
        self.send(recipients=recipients, subject=subject, content=content)




def send_email_notification(username, first_name, last_name, file_base64, file_name, errors):
    file = base64.b64decode(file_base64)
    load_dotenv(f"{BASE_DIR}/.env")
    # получаем name, email активных получателей уведомлений, если у email есть значение
    notification_recipients = get_email_notification_recipients()

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



