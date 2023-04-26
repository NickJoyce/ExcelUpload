from .context_manager import db

def get_email_notification_recipients():
    with db() as cursor:
        cursor.execute("""SELECT name, email FROM app_notificationrecipients 
                          WHERE is_active=%s AND email IS NOT NULL""", (True,))
        return cursor.fetchall()

def get_telegram_notification_recipients():
    with db() as cursor:
        cursor.execute("""SELECT name, telegram_id FROM app_notificationrecipients 
                		  WHERE is_active=%s AND telegram_id IS NOT NULL""", (True,))
        return cursor.fetchall()

def get_username_first_name_last_name(user_id):
    with db() as cursor:
        cursor.execute("""SELECT u.username, u.first_name, u.last_name 
                		  FROM auth_user AS u
                		  JOIN app_profile AS p
                		  ON u.id=p.user_id
                		  WHERE u.id=%s""", (user_id,))
        return cursor.fetchall()[0]



if __name__ == "__main__":
    print(get_email_notification_recipients())