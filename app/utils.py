import os
import pandas as pd
from .models import Marketplace, PickupPoint
from django.contrib import messages

class File:
    def __init__(self, th, file_path, form_ident, input_accept):
        self.th = th
        self.file_path = file_path
        self.form_ident = form_ident
        self.input_accept = input_accept
        self.file_name = self.get_file_name(self.file_path)


    @staticmethod
    def get_file_name(file_path):
        try:
            file_name = os.listdir(file_path)[0] if os.listdir(file_path)[0] != ".gitkeep" else os.listdir(file_path)[1]
        except IndexError:
            file_name = "---файл не загружен---"
        return file_name

def pickup_points_file_handling(request, file):
    dataframes = pd.read_excel(file, None)
    marketplaces = Marketplace.objects.all()
    updated_marketplaces = []
    for sheet_name, df in dataframes.items():
        for marketplace in marketplaces:
            if sheet_name == marketplace.name:
                # удаляем все ПВЗ этого маркетплейса
                PickupPoint.objects.filter(marketplace=marketplace).delete()
                for row in df.itertuples():
                    # создаем объекты ПВЗ
                    PickupPoint.objects.create(marketplace=marketplace, address=row.Адрес)
                updated_marketplaces.append(marketplace.name)
    messages.add_message(request, messages.SUCCESS, f'Обновлены ПВЗ для следующих маркетплейсов: {updated_marketplaces}')