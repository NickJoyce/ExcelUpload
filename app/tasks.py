from project.celery import app
from .excel_file_handling.main import make_handling
import requests


import base64
from project.settings import BASE_DIR
from smtplib import SMTP_SSL
from email.message import EmailMessage
import os
from database.context_manager import db
from dotenv import load_dotenv

@app.task
def make_handling_task(user_id, file_base64, file_name):
    make_handling(user_id, file_base64, file_name)

