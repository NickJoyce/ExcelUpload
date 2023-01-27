from project.celery import app
from .excel_file_handling.main import make_handling
import requests


@app.task
def make_handling_task(user_id, file_base64, file_name):
    print("Сломано!")
    # make_handling(user_id, file_base64, file_name)

