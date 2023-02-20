***Addition info***
1. В административной панеле необходимо создать группу "Клиенты"
ПОЛЬЗОВАТЕЛИ И ГРУППЫ -> Группы -> ДОБАВИТЬ ГРУППА 
Имя (строго): "Клиенты"
Права: можно не добавлять

2. При создании пользователя необходимо добавлять его в группу "Клиенты"

3. Создание json объекта вариаций заголовков
APP -> Настрока вариаций наименования -> Добавить Настрока вариаций наименования
Имя (строго): Вариации наименования заголовков
Значения только в нижнем регистре

Пример json:
```json
{
  "required_fields": {
    "receiver_name": ["имя", "фио"],
    "code": ["код выдачи", "код" ],
    "phone": ["телефон", "номер телефона"],
    "address": ["адрес", "пункт выдачи"]
  },
  "unrequired_fields": {
    "sku": ["артикул","sku"],
    "size": ["размер", "размер товара"],
    "product_name": ["товар"],
    "status": ["cтатус"],
    "price": ["цена товара"]
  }
}
```

4. Создание json объекта вариаций листов
APP ->  Настрока вариаций наименования -> Добавит Настрока вариаций наименования
Имя (строго): Вариации наименования листов
В обработку берется первый совпавший

Пример json:
```json
{
  "possible_sheet_names": ["Без заголовков"]
}
```


4. Создание json объекта вариаций листов
APP ->  Настрока вариаций наименования -> Добавит Настрока вариаций наименования
Имя (строго): Плохие значения размера
В обработку берется первый совпавший

Пример json:
```json
{
  "bad_size_value": ["без размера", "нет размера"]
}
```


5. Создание json объекта даты и времени загрузки
APP ->  Настроки дат и времени	-> ДОБАВИТЬ НАСТРОКА ДАТ И ВРЕМЕНИ
Имя (строго): Загрузка файла

Пример json:
```json
{
  "end_time": {
    "hour": 14,
    "minute": 0,
    "second": 0
  },
  "holidays": [
    7
  ],
  "start_time": {
    "hour": 8,
    "minute": 0,
    "second": 0
  },
  "error_text": "Файл не загружен! Загрузка доступна с 8:00 до 14:00, ПН-СБ"
}
```

6. Создание страниц 
APP -> Страницы -> ДОБАВИТЬ СТРАНИЦА
    [НАИМЕНОВАНИЕ СТРАНИЦЫ 
    ФУНКЦИЯ-ОБРАБОТЧИК 
    HTML ФАЙЛ]

    - [Загрузка файла Excel	  -  excel_upload	-   excel_upload.html]
    - [Статусы заказов   -   order_statuses   -   order_statuses.html]
    - [Поставка на склад   -   supply   -   supply.html]
    - [Список адресов ПВЗ   -   pickup_point_list   -   pickup_point_list.html]
    - [Главная   -   index   -   index html]


7. Доступ в терминал работающий в фоне: tmux attach -t celery_admin

8. Создать группу "Клиенты"

9. Внутри файлов 
FILE_LOCATIONS = {
    "agreement": os.path.join(BASE_DIR, 'app', 'files', 'agreement'),
    "pickup_points": os.path.join(BASE_DIR, 'app', 'files', 'pickup_points')
}
перед диплоем необходимо удалить все файлы и поместить в каждую папку файл .gitkeep
для того чтобы папки загружались на гит, на проде лежат файлы загруженные пользователем 
при git pull на сервере они будут добавлены в эту папку

10. Загрузка excel файла с ПВЗ 
Файлы загружаются на странице "Загрузка файлов" админки

Структура документа Excel:
1. Название листов равны значению полей "Наименование маркетплейса" в пункте "Маркетплейсы" админки
2. Каждый лист должен содержать заголовок 'Адрес'
Регистр имеет значение

Логика:
При загрузке файла сравниваются имена экземпляров маркетплейсов в бд и наименования 
листов в файле эксель. Если совпадения найдено то удаляются все текущие ПВЗ этого маркетрлейса и заново 
создаются новые ПВЗ. Добавляются только поля маркетплейса и адрес, все остальные поля обнуляются.

Сайт:
 Отображаются данные из БД (маркетплейс + ПВЗ). Если файл не загружен выведется соответствующая ошибка.
