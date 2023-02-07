import requests
import base64
from project.settings.base import BASE_DIR
import os
from database.context_manager import db
from dotenv import load_dotenv

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


if __name__ == "__main__":
    ...







# def send_msg(username, first_name, last_name, chat_id):
#     text = f"Пользователь {username} ({first_name} {last_name}) загрузил файл:"
#     requests.get(f"{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}")
#
#
# def send_file(file_name, chat_id):
#     files = {'docement': open(f"{file_name}", "rb")}
#     res = requests.get(f"{URL}{TOKEN}/sendDocument?chat_id={chat_id}", files=files)
#     print(res.text)
#     # return file_copy
