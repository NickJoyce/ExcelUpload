import requests
import xml.etree.ElementTree as ET

request = """<?xml version="1.0" encoding="UTF-8" ?>
<statusreq>
  <auth extra="26" login="GAPS" pass="VfX-UBQ-Rn6-b5v"></auth>
  <datefrom>2022-12-30</datefrom>
  <dateto>2022-12-31</dateto>
</statusreq>"""

response = requests.post("https://home.courierexe.ru/api/", data=request.encode())
print(response.text)

root = ET.fromstring(response.text)

for order in root.findall('order'):
    date = order.find('receiver').find('date').text
    receiver_name = order.find('receiver').find('company').text
    address = order.find('receiver').find('address').text
    phone = order.find('receiver').find('phone').text
    code = order.find('receiver').find('person').text
    sku_size  = order.find('enclosure').text
    product_name = order.find('instruction').text
    status = order.find('deliveredto').text

    print(date, "|", receiver_name, "|", address, "|",phone, "|", code, "|", sku_size, "|", product_name, "|", status)