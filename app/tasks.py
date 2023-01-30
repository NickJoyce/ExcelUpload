from project.celery import app
from .excel_file_handling.main import make_handling
import requests
import traceback
from database.context_manager import db

from .excel_file_handling.notifications.e_mail import send_email_notification
from .excel_file_handling.notifications.telegram import send_telegram_notification


@app.task
def make_handling_task(user_id, file_base64, file_name):
    try:
        make_handling(user_id, file_base64, file_name)
    except:
        with db() as cursor:
            cursor.execute("""SELECT u.username, u.first_name, u.last_name 
                    		  FROM auth_user AS u
                    		  JOIN app_profile AS p
                    		  ON u.id=p.user_id
                    		  WHERE u.id=%s""", (user_id,))
            username, first_name, last_name = cursor.fetchall()[0]
            errors = [f"Ошибка приложения\n{traceback.format_exc()}"]
            send_telegram_notification(username, first_name, last_name, file_base64, file_name, errors)
            send_email_notification(username, first_name, last_name, file_base64, file_name, errors)





