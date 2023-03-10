import os
from celery import Celery
from dotenv import load_dotenv


load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.dev")

# указываем project_name
app = Celery("project")
# указываем что конфигурацию нужно брать из файла настроек django
# имена соответствующих переменных должны начинаться с CELERY
app.config_from_object("django.conf:settings", namespace="CELERY")
# таски будут находиться автоматически в файле tasks.py приложения
app.autodiscover_tasks()


