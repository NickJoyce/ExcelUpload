from database.context_manager import db
from pandas.core.frame import DataFrame

import pandas as pd


def sheet_name_check(file, df = None) -> DataFrame or None:
    # выбор наименования листа
    with db() as cursor:
        cursor.execute("""SELECT obj FROM app_jsonobject WHERE name=%s""", ("Вариации наименования листов",))
        possible_sheet_names = cursor.fetchall()[0][0]['possible_sheet_names']
        for n, name in enumerate(possible_sheet_names, start=1):
            try:
                df = pd.read_excel(file, sheet_name=name)
                break
            except ValueError:
                # если последний элемнт а списке
                if n == len(possible_sheet_names):
                    df = pd.read_excel(file)
                else:
                    continue
        return df.fillna("")


def get_match_headers(current_headers, header_name_variations) -> dict:
    """
    Возвращает словарь:
    ключ - имя требуемого поля (на которое переиминуем заголовк датафрейма)
    значение - имя поля в таблце экселе или None если его нет
    """
    res = {}
    for field_name, variations_list in header_name_variations.items():
        res[field_name] = None
        for variant in variations_list:
            for header in current_headers:
                if variant == header.lower():
                    res[field_name] = header
                    break
    return res


def get_duplicate_headers(match_headers, current_headers):
    current_headers = [ current_header.split('.')[0] for current_header in current_headers]
    dup = []
    for match_header in match_headers:
        if current_headers.count(match_header) > 1:
            dup.append(match_header)
    return dup if dup else None


if __name__ == "__main__":
    ...
