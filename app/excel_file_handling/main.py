import base64
from .checker import sheet_name_check, get_match_headers, get_duplicate_headers
from database.context_manager import db
from .utils import get_orders, send_request
from .notifications.e_mail import send_email_notification
from .notifications.telegram import send_telegram_notification


def make_handling(user_id, file_base64, file_name):
    with db() as cursor:
        # файл (bytes)
        file = base64.b64decode(file_base64)

        # загрузка данных клиента по id
        cursor.execute("""SELECT u.username, u.first_name, u.last_name, 
                                 p.xml_api_extra, p.xml_api_login, p.xml_api_password
        				  FROM auth_user AS u
        				  JOIN app_profile AS p
        				  ON u.id=p.user_id
        				  WHERE u.id=%s""", (user_id,))
        username, first_name, last_name, xml_api_extra, xml_api_login, xml_api_password = cursor.fetchall()[0]

        # проверка имени листов с возвратом датайрейма
        df = sheet_name_check(file)


        # проверяем коректность заголовков таблицы
        current_headers = list(df)
        # print("Текущие заголовки: ", current_headers)

        cursor.execute("""SELECT obj FROM app_jsonobject WHERE name=%s""", ("Вариации наименования заголовков",))
        header_name_variations: dict = cursor.fetchall()[0][0]

        # варианты наименований для обязательных заголовков
        header_name_variations_req: dict = header_name_variations['required_fields']

        # варианты наименований для необязательных заголовков
        header_name_variations_unreq: dict = header_name_variations['unrequired_fields']
        # print("Варианты наименований для необязательных заголовков: ", header_name_variations_unreq)

        # совпадение текущих заголовков датафрейма и вариантов наименований обязательных заголовков (json)
        req_match: dict = get_match_headers(current_headers, header_name_variations_req)

        # совпадение текущих заголовков датафрейма и вариантов наименований необязательных заголовков (json)
        unreq_match: dict = get_match_headers(current_headers, header_name_variations_unreq)
        # print("Совпадение текущих заголовков датафрейма и вариантов наименований необязательных заголовков : ", unreq_match)

        # совпавшие обязательные и необязательные заголовки
        match_headers = list(req_match.values()) + list(unreq_match.values())



        # наличие дубликатов наименований заголовков
        dup: set or None = get_duplicate_headers(match_headers, current_headers)

        errors = []

        # если не у всех обязательных заголовков найдены совпадения:
        if not all(list(req_match.values())):
            for json_key_header, current_header in req_match.items():
                if current_header == None:
                    errors.append(f"Наименования столбца [ {json_key_header} ] нет в списке совпадений.")


        # дубликаты
        if dup:
            dup = ", ".join(dup)
            errors.append(f"В загружаемом файле Excel есть дубликаты наименований слудующих столбцов: [ {dup} ]")


        if not errors:
            # переименовываем все заголовки датафрейма для обязательных полей
            for new_name, old_name in req_match.items():
                df.rename(columns={old_name: new_name}, inplace=True)

            # переименовывам все заголовки датафрейма для необязательных полей если они есть
            for new_name, old_name in unreq_match.items():
                if old_name:
                    df.rename(columns={old_name: new_name}, inplace=True)

            # формируем список заказов подлежащих загрузке чере API
            orders = get_orders(df)
            for order in orders:
                ...
                # print("-"*50)
                # print(order.receiver_name)
                # print(order.code)
                # print(order.phone)
                # print(order.address)
                # print(order.sku)
                # print(order.size)
                # print(order.product_name)
                # print(order.status)
                # print(order.price)
                # print("-" * 50)

            # отправка запроса
            send_request(orders, username, first_name, last_name, xml_api_extra, xml_api_login, xml_api_password)

        else:
            send_telegram_notification(username, first_name, last_name, file_base64, file_name, errors)

        send_email_notification(username, first_name, last_name, file_base64, file_name, errors)
