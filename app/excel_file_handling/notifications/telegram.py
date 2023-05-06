import requests
import base64
from project.settings.base import BASE_DIR
import os
from database.context_manager import db
from dotenv import load_dotenv

from database.queries import get_telegram_notification_recipients



class TelegramBotNotification():
    def __init__(self):
        self.tg_bot_url = os.getenv('TG_BOT_URL')
        self.tg_bot_token = os.getenv('TG_EXCEL_UPLOAD_BOT_TOKEN')

    def send(self, recipients, subject, content, file=None):
        """recipients - tuple содержит 2 элемента: имя и telegram_id получателя"""
        for name, telegram_id in recipients:
            requests.get(f"{self.tg_bot_url}{self.tg_bot_token}/sendMessage?chat_id={telegram_id}&text={subject + content}")


    def supply_order_sucessfully_created(self, username, first_name, last_name, sales_channel, comment,
                                         recipient_address,recipient_full_name, recipient_phone):
        recipients = get_telegram_notification_recipients()
        subject = f"[NEW ORDER]\n\n"
        content = f"Пользователь: {username} ({first_name} {last_name})\n\n" \
                  f"ДАННЫЕ ЗАКАЗА:\n" \
                  f"Канал продаж: {sales_channel}\n" \
                  f"Адрес: {recipient_address}\n" \
                  f"ФИО: {recipient_full_name}\n" \
                  f"Телефон: {recipient_phone}\n" \
                  f"Комментарий: {comment}"
        self.send(recipients=recipients, subject=subject, content=content)


    def counterparty_id_is_not_exist(self, username, first_name, last_name, sales_channel, comment, recipient_address,
                                                       recipient_full_name, recipient_phone, counterparty_id):
        recipients = get_telegram_notification_recipients()
        subject = f"[COUNTERPARTY DOES NOT EXIST]\n\n"
        content = f"Контрагента с id={counterparty_id} не существует.\n\n" \
                  f"Пользователь: {username} ({first_name} {last_name})\n\n" \
                  f"ДАННЫЕ ЗАКАЗА:\n" \
                  f"Канал продаж: {sales_channel}\n" \
                  f"Адрес: {recipient_address}\n" \
                  f"ФИО: {recipient_full_name}\n" \
                  f"Телефон: {recipient_phone}\n" \
                  f"Комментарий: {comment}"
        self.send(recipients=recipients, subject=subject, content=content)


    def general_error(self, username, first_name, last_name, error):
        recipients = get_telegram_notification_recipients()
        subject = f"[APP ERROR]\n[ {username} ({first_name} {last_name}) ]\n"
        content = f"{error}"
        self.send(recipients=recipients, subject=subject, content=content)

    def error_in_the_response_body_when_creating_an_order(self, username, first_name, last_name, errors):
        recipients = get_telegram_notification_recipients()
        subject = f"[ERRORS IN THE RESPONSE BODY]\n[ {username} ({first_name} {last_name}) ]\n"
        content = f"{errors}\n" \
                  f"ДАННЫЕ НЕ БЫЛИ ЗАГРУЖЕНЫ В МОЙСКЛАД ДЛЯ ЗАКАЗА\n" \
                  f"↓↓↓↓↓↓↓"
        self.send(recipients=recipients, subject=subject, content=content)




def get_tg_bot_url():
    load_dotenv(f"{BASE_DIR}/.env")
    return os.getenv('TG_BOT_URL')

def get_tg_excel_upload_bot_token():
    load_dotenv(f"{BASE_DIR}/.env")
    return os.getenv('TG_EXCEL_UPLOAD_BOT_TOKEN')

def send_telegram_notification(username, first_name, last_name, file_base64, file_name, errors):
    with db() as cursor:
        url = get_tg_bot_url()
        token = get_tg_excel_upload_bot_token()

        file = base64.b64decode(file_base64)
        path = f'{file_name}'
        # записываем файл во временную папку
        # по хорошему нужно понять как отправлять bytes напрямую не сохраняя
        with open(path, 'wb') as f:
            f.write(file)

        # получаем name,telegram_id активных получателей уведомлений, если у telegram_id есть значение
        cursor.execute("""SELECT name, telegram_id FROM app_notificationrecipients 
        						  WHERE is_active=%s AND telegram_id IS NOT NULL""", (True,))
        notification_recipients = cursor.fetchall()


        for name, telegram_id in notification_recipients:
            # отправка сообщения
            subject = f"[FAIL]\n[ {username} ({first_name} {last_name}) ]\nЗаказы из файла не загружены\n"
            # текст письма
            content = "Произошли следующие ошибки:\n"
            for error in errors:
                content += "- " + error + '\n'

            requests.get(f"{url}{token}/sendMessage?chat_id={telegram_id}&text={subject + content}")

            # отправка файла
            files = {'document': open(path, "rb")}
            res = requests.get(f"{url}{token}/sendDocument?chat_id={telegram_id}", files=files)
            # print(res.text)
            # print(file_name)
        os.remove(path)




def send_signup_telegram_notification(username, company, first_name, last_name, phone, email):
    with db() as cursor:
        url = get_tg_bot_url()
        token = get_tg_excel_upload_bot_token()
        # получаем name,telegram_id активных получателей уведомлений, если у telegram_id есть значение
        cursor.execute("""SELECT name, telegram_id FROM app_notificationrecipients 
        						  WHERE is_active=%s AND telegram_id IS NOT NULL""", (True,))
        notification_recipients = cursor.fetchall()
        for name, telegram_id in notification_recipients:
            # отправка сообщения
            content = f"[NEW REGISTRATION]\n" \
                      f"Имя пользователя: {username}\n" \
                      f"Компания: {company}\n" \
                      f"Имя: {first_name}\n" \
                      f"Фамилия: {last_name}\n" \
                      f"Телефон: {phone}\n" \
                      f"Email: {email}\n"
            requests.get(f"{url}{token}/sendMessage?chat_id={telegram_id}&text={content}")


def send_supply_telegram_notification(username, first_name, last_name, marketplace_address, supply_date):
    with db() as cursor:
        url = get_tg_bot_url()
        token = get_tg_excel_upload_bot_token()
        # получаем name,telegram_id активных получателей уведомлений, если у telegram_id есть значение
        cursor.execute("""SELECT name, telegram_id FROM app_notificationrecipients 
        						  WHERE is_active=%s AND telegram_id IS NOT NULL""", (True,))
        notification_recipients = cursor.fetchall()
        for name, telegram_id in notification_recipients:
            # отправка сообщения
            content = f"[NEW SUPPLY ORDER]\n" \
                      f"Имя пользователя: {username}\n" \
                      f"Имя: {first_name}\n" \
                      f"Фамилия: {last_name}\n" \
                      f"Склад: {marketplace_address}\n" \
                      f"Дата: {supply_date}\n"
            requests.get(f"{url}{token}/sendMessage?chat_id={telegram_id}&text={content}")


def send_xml_errors_telegram_notification(errors, username, first_name, last_name):
    with db() as cursor:
        url = get_tg_bot_url()
        token = get_tg_excel_upload_bot_token()
        # получаем name,telegram_id активных получателей уведомлений, если у telegram_id есть значение
        cursor.execute("""SELECT name, telegram_id FROM app_notificationrecipients 
        						  WHERE is_active=%s AND telegram_id IS NOT NULL""", (True,))
        notification_recipients = cursor.fetchall()
        content = f"Ошибки выполнения запросов у {username} ({first_name} {last_name}):\n"
        for name, telegram_id in notification_recipients:
            # отправка сообщения
            content += "\n".join(errors)
            requests.get(f"{url}{token}/sendMessage?chat_id={telegram_id}&text={content}")


def supply_order_successfully_created():
    recipients = get_telegram_notification_recipients()
    subject = "test"
    content = "test"
    TelegramBotNotification().send(recipients=recipients, subject=subject, content=content)






if __name__ == "__main__":
    supply_order_successfully_created()



