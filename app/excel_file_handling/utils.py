import os
import requests
from jinja2 import Template
from project.settings.base import BASE_DIR
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
from database.context_manager import db
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from .notifications.telegram import send_xml_errors_telegram_notification


class Order():
    def __init__(self, receiver_name, code, phone, address, date,
                 sku="", size="", product_name="", status="", price="", sku_size=None):
        self._receiver_name = receiver_name
        self._code = code
        self._phone = phone
        self._address = address
        self._date = date
        self._sku = sku
        self._size = size
        self._product_name = product_name
        self._status = status
        self._price = price
        self.sku_size = sku_size


    @property
    def receiver_name(self):
        return self._receiver_name

    @receiver_name.setter
    def receiver_name(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._receiver_name = value


    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._code = value


    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._phone = value


    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._address = value


    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._date = value


    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._sku = value


    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._size = value


    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._product_name = value


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._status = value


    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value and isinstance(value, str):
            value = self.replace_xml_unsuitable_simbols_in_string(value)
        self._price = value


    def __str__(self):
        return f"Order({self.receiver_name}, {self.code}, {self.phone}, {self.address}, {self.date}, {self.sku}," \
               f"{self.size}, {self.product_name}, {self.status}, {self.price})"


    @staticmethod
    def replace_xml_unsuitable_simbols_in_string(str_):
        replace_list = [("&", "&amp;"),
                        ("<", "&lt;"),
                        (">", "&gt;"),
                        ("\"", "&quot;")]
        for i in replace_list:
            if i[0] in str_:
                str_ = str_.replace(i[0], i[1])
        return str_



def get_orders(df):
    with db() as cursor:
        cursor.execute("""SELECT obj FROM app_jsonobject WHERE name=%s""", ("Плохие значения размера",))
        bad_size_value = cursor.fetchall()[0][0]['bad_size_value']

    if df.iat[0,0] == "Обратите внимание! Пакеты на ПВЗ платные, стоимость одного пакета от 8 до 15 рублей. " \
                      "Рекомендуем при заборе товаров пользоваться собственными пакетами.":
        df.drop(axis=0, index=0, inplace=True)

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

            try:
                order.code = str(int(order.code))
            except ValueError:
                raise ValueError("Неверный формат кода выдачи")

            if len(order.code) == 1:
                order.code = "00" + order.code
            elif len(order.code) == 2:
                order.code = "0" + order.code
            else:
                pass

            if isinstance(order.phone, float):
                order.phone = str(int(order.phone))
            elif isinstance(order.phone, int):
                order.phone = str(order.phone).strip()

            if "-" in order.phone:
                order.phone = order.phone.replace("-", "")

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


def send_request(orders, username, first_name, last_name, extra, login, password):
    load_dotenv(f"{BASE_DIR}/.env")
    with open(f"{BASE_DIR}/request.xml", encoding="utf-8") as f:
        xml_file = f.read()
        rendered_template = Template(xml_file).render(
                      extra = extra.strip(),
                      login = login.strip(),
                      password = password.strip(),
                      orders = orders)
        response = requests.post(os.getenv("API_PATH"), data = rendered_template.encode())

        tree = ET.fromstring(response.text)
        errors = []
        for n, createorder in enumerate(tree.findall('createorder'), 1):
            error_msg = createorder.get('errormsgru')
            if not error_msg == "Успешно":
                errors.append(f"[{n}] {error_msg}")
        if errors:
            send_xml_errors_telegram_notification(errors[:5], username, first_name, last_name,)

        print(response.text)



def send_order_statuses_request(extra, login, password, datefrom, dateto):
    load_dotenv(f"{BASE_DIR}/.env")
    with open(f"{BASE_DIR}/order_statuses_request.xml", encoding="utf-8") as f:
        xml_file = f.read()
        rendered_template = Template(xml_file).render(
            extra=extra.strip(),
            login=login.strip(),
            password=password.strip(),
            datefrom=datefrom,
            dateto=dateto
        )
        response = requests.post(os.getenv("API_PATH"), data=rendered_template.encode())
        return response

def handling_order_statuses_request(response):
    root = ET.fromstring(response.text)
    orders_data = []
    for order in root.findall('order'):
        status = order.find('deliveredto').text
        status = status if status else "В работе"
        current_order = Order(
        date = order.find('receiver').find('date').text,
        receiver_name = order.find('receiver').find('company').text,
        address = order.find('receiver').find('address').text,
        phone = order.find('receiver').find('phone').text,
        code = order.find('receiver').find('person').text,
        sku_size = order.find('enclosure').text,
        product_name = order.find('instruction').text,
        status = status
        )
        orders_data.append(current_order)
    return orders_data


def send_supply_order_request(extra, login, password, supply_date, marketplace, address):
    load_dotenv(f"{BASE_DIR}/.env")
    with open(f"{BASE_DIR}/supply_order_request.xml", encoding="utf-8") as f:
        xml_file = f.read()
        rendered_template = Template(xml_file).render(
                      extra=extra.strip(),
                      login=login.strip(),
                      password=password.strip(),
                      supply_date=supply_date,
                      marketplace=marketplace,
                      address=address)
        response = requests.post(os.getenv("API_PATH"), data = rendered_template.encode())
        print(response.text)



if __name__ == "__main__":
    response = send_order_statuses_request(extra='26',
                                login="GAPS",
                                password="VfX-UBQ-Rn6-b5v",
                                datefrom="2023-01-29",
                                dateto="2023-01-30")
    print(handling_order_statuses_request(response))

