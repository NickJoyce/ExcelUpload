import requests
import json
from jinja2 import Template
from project.settings.base import BASE_DIR
from project.settings.base import MOYSKLAD_TOKEN, MOYSKLAD_ORGANIZATION_ID


class SaleChannel():
    def __init__(self, id, name):
        self.id = id
        self.name = name


def get_saleschannel(saleschannel_id):
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/saleschannel/{saleschannel_id}"
    headers = {'Authorization': f'Bearer {MOYSKLAD_TOKEN}', 'Content-Type': 'application/json'}
    response = requests.get(url=url, headers=headers)
    return response.json()['name']




def create_counterparty(first_name, last_name, email, phone, company, inn) -> str:
    url = "https://online.moysklad.ru/api/remap/1.2/entity/counterparty"
    headers = {'Authorization': f'Bearer {MOYSKLAD_TOKEN}', 'Content-Type': 'application/json'}
    data = {"legalFirstName": first_name,
            "legalLastName": last_name,
            "email": email,
            "phone": phone,
            "name": company,
            "inn": inn}
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    return response.json()['id']




def is_counterparty(counterparty_id, token=MOYSKLAD_TOKEN):
    url = f"https://online.moysklad.ru/api/remap/1.2/entity/counterparty/{counterparty_id}"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    response = requests.get(url=url, headers=headers)
    if "errors" in response.json():
        return False
    else:
        return True


def create_order(sales_channel_id,
                 comment,
                 recipient_address,
                 recipient_full_name,
                 recipient_phone,
                 counterparty_id,
                 organization_id=MOYSKLAD_ORGANIZATION_ID,
                 token=MOYSKLAD_TOKEN):
    url = "https://online.moysklad.ru/api/remap/1.2/entity/customerorder"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    with open(f"{BASE_DIR}/app/moysklad/templates/order.json", encoding="utf-8") as f:
        file = f.read()
        rendered_template = Template(file).render(
            organization_id=organization_id,
            sales_channel_id=sales_channel_id,
            comment=comment,
            recipient_address=recipient_address,
            recipient_full_name=recipient_full_name,
            recipient_phone=recipient_phone,
            counterparty_id=counterparty_id
        )
        response = requests.post(url=url, headers=headers, data=rendered_template.encode())


if __name__ == "__main__":
    # create_order(sales_channel_id = "037e61d7-d23a-11ed-0a80-0f0f0000022f",
    #              comment = "here is comment",
    #              recipient_address = "recipient address",
    #              recipient_full_name = "recipient full name",
    #              recipient_phone = "recipient phone",
    #              counterparty_id="d24bf4b6-e039-11ed-0a80-0f410016e6a0")
    # print(is_counterparty("d24bf4b6-e039-11ed-0a80-0f410016e6a0"))
    print(get_saleschannel('037e61d7-d23a-11ed-0a80-0f0f0000022f'))
    ...