import os
import requests
from jinja2 import Template
from project.settings import BASE_DIR
from datetime import datetime
import pandas as pd


class Order():
    def __init__(self, receiver_name, code, phone, address, date,
                 sku="", size="", product_name="", status=""):
        self.receiver_name = receiver_name
        self.code = code
        self.phone = phone
        self.address = address
        self.date = date
        self.sku = sku
        self.size = size
        self.product_name = product_name
        self.status = status

    def __str__(self):
        return f"Order({self.receiver_name}, {self.code}, {self.phone}, {self.address}, {self.date}, {self.sku}," \
               f"{self.size}, {self.product_name}, {self.status})"



def get_orders(df):
    orders = []
    for row in df.itertuples():
        if all([pd.notna(row.receiver_name), pd.notna(row.code), pd.notna(row.phone), pd.notna(row.address)]):
            order = Order(receiver_name = row.receiver_name,
                          code = row.code,
                          phone = row.phone,
                          address = row.address,
                          date = datetime.now().strftime('%Y-%m-%d'))

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

            order.code = "00" + str(order.code)
            order.phone = "т.:" + str(order.phone).strip()[-4:]

            if order.status:
                if order.status.lower().startswith('готов'):
                    orders.append(order)
            else:
                orders.append(order)
    return orders


def send_request(orders, extra, login, password):
    with open(f"{BASE_DIR}/app/excel_file_handling/request.xml") as f:
        xml_file = f.read()
        rendered_template = Template(xml_file).render(
                      extra = extra,
                      login = login,
                      password = password,
                      orders = orders)
        response = requests.post("https://home.courierexe.ru/api/", data = rendered_template.encode('utf-8'))
        print(response.text)
