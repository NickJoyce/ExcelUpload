from project.celery import app
from .excel_file_handling.main import make_handling
from .moysklad.utils import is_counterparty, create_order, get_saleschannel
import traceback
from database.queries import get_username_first_name_last_name


from .excel_file_handling.notifications.e_mail import send_email_notification
from .excel_file_handling.notifications.telegram import send_telegram_notification


from .excel_file_handling.notifications.e_mail import EmailNotification
from .excel_file_handling.notifications.telegram import TelegramBotNotification








@app.task
def make_handling_task(user_id, file_base64, file_name):
    print("make_handling_task")
    try:
        make_handling(user_id, file_base64, file_name)
    except:
        username, first_name, last_name = get_username_first_name_last_name(user_id)
        errors = [f"Ошибка приложения\n{traceback.format_exc()}"]
        send_telegram_notification(username, first_name, last_name, file_base64, file_name, errors)
        send_email_notification(username, first_name, last_name, file_base64, file_name, errors)


@app.task
def send_order_to_moysklad_task(user_id,
                                sales_channel_id,
                                comment,
                                recipient_address,
                                recipient_full_name,
                                recipient_phone,
                                counterparty_id):
    username, first_name, last_name = get_username_first_name_last_name(user_id)
    sales_channel = get_saleschannel(sales_channel_id)
    if is_counterparty(counterparty_id):
        try:
            create_order(sales_channel_id=sales_channel_id,
                         comment=comment,
                         recipient_address=recipient_address,
                         recipient_full_name=recipient_full_name,
                         recipient_phone=recipient_phone,
                         counterparty_id=counterparty_id)
            args = [username, first_name, last_name, sales_channel, comment, recipient_address, recipient_full_name,
                    recipient_phone,]
            EmailNotification().supply_order_sucessfully_created(*args)
            TelegramBotNotification().supply_order_sucessfully_created(*args)
        except:
            TelegramBotNotification().general_error(username, first_name, last_name, traceback.format_exc())
            EmailNotification().general_error(username, first_name, last_name, traceback.format_exc())
    else:
        args = [username, first_name, last_name, sales_channel, comment, recipient_address, recipient_full_name,
                recipient_phone,counterparty_id]
        EmailNotification().counterparty_id_is_not_exist(*args)
        TelegramBotNotification().counterparty_id_is_not_exist(*args)

