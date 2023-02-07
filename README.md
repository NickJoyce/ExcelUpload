# Client's personal account

Personal account for courier service clients

## Quickstart

***Run the following commands to bootstrap your environment:***

    sudo apt install software-properties-common -y  
    sudo add-apt-repository ppa:deadsnakes/ppa  
    sudo apt install python3.10
    
    sudo apt install git python3-dev python3-venv python3-pip nginx postgresql postgresql-contrib redis-server tmux
    
    git clone https://github.com/NickJoyce/ExcelUpload
    cd ExcelUpload
    
    scp /home/nick/Desktop/ExcelUpload/.env main@45.141.77.146:~/ExcelUpload
    
    python3.10 -m venv venv  
    . venv/bin/activate  
    pip install --upgrade pip  
    pip install -r requirements.txt
    
    set project.settings.prod instead project.settings in manage.py, project/celery.py, project/wsgi.py
    
    python manage.py makemigrations
    python manage.py migrate
    
    python manage.py collectstatic --settings=project.settings.prod
    
    tmux new -s celery_admin / tmux attach -t celery_admin 
    . venv/bin/activate
    celery -A project worker -l info
    ^b + d to exit

    


***Run the app locally***

    python3 manage.py runserver 0.0.0.0:8000 --settings=project.settings.dev

***Run the app with Gunicorn***

    gunicorn project.wsgi -b 0.0.0.0:8001

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

