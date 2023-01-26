import os
import requests
from jinja2 import Template
from project.settings import BASE_DIR
from datetime import datetime
from datetime import timedelta
import pandas as pd
from database.context_manager import db
from dotenv import load_dotenv


class Order():
    def __init__(self, receiver_name, code, phone, address, date,
                 sku="", size="", product_name="", status="", price=""):
        self.receiver_name = receiver_name
        self.code = code
        self.phone = phone
        self.address = address
        self.date = date
        self.sku = sku
        self.size = size
        self.product_name = product_name
        self.status = status
        self.price = price

    def __str__(self):
        return f"Order({self.receiver_name}, {self.code}, {self.phone}, {self.address}, {self.date}, {self.sku}," \
               f"{self.size}, {self.product_name}, {self.status}, {self.price})"



def get_orders(df):
    with db() as cursor:
        cursor.execute("""SELECT obj FROM app_jsonobject WHERE name=%s""", ("Плохие значения размера",))
        bad_size_value = cursor.fetchall()[0][0]['bad_size_value']

    orders = []
    for row in df.itertuples():
        if all([pd.notna(row.receiver_name), pd.notna(row.code), pd.notna(row.phone), pd.notna(row.address)]):

            date = datetime.now()
            weekday = datetime.weekday(datetime.now())
            if weekday in [5, 6]:
                date = date + timedelta(days=2)
            date = date.strftime('%Y-%m-%d')

            order = Order(receiver_name = row.receiver_name,
                          code = row.code,
                          phone = row.phone,
                          address = row.address,
                          date = date)

            # проверяем есть ли столбцы в датафрейме для необязательных полей
            try:
                order.sku = row.sku
            except AttributeError:
                pass

            try:
                order.size = row.size
            except AttributeError:
                pass

            try:
                order.product_name = row.product_name
            except AttributeError:
                pass

            try:
                order.status = row.status
            except AttributeError:
                pass

            try:
                order.price = row.price
            except AttributeError:
                pass


            if order.size:
                if str(order.size).lower() in bad_size_value:
                        order.size = ""



            order.code = str(int(order.code))

            if len(order.code) == 1:
                order.code = "00" + order.code
            elif len(order.code) == 2:
                order.code = "0" + order.code
            else:
                pass

            if isinstance(order.phone, float):
                order.phone = str(int(order.phone))

            order.phone = "т.:" + str(order.phone).strip()[-4:]


            if order.sku:
                if isinstance(order.sku, float):
                    order.sku = str(int(order.sku))


            if order.status:
                if order.status.lower().startswith('готов'):
                    orders.append(order)

            else:
                orders.append(order)
    return orders


def send_request(orders, extra, login, password):
    load_dotenv(f"{BASE_DIR}/.env")
    with open(f"{BASE_DIR}/request.xml", encoding="utf-8") as f:
        xml_file = f.read()
        rendered_template = Template(xml_file).render(
                      extra = extra.strip(),
                      login = login.strip(),
                      password = password.strip(),
                      orders = orders)
        response = requests.post(os.getenv("API_PATH"), data = rendered_template.encode())
        print(response.text)


