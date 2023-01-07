import psycopg2
from project.settings import DATABASES
from project.settings import BASE_DIR
import os
from dotenv import load_dotenv


class db:
	"""Диспетчер контекста для подключения БД"""
	def __init__(self) -> None:
		self.configuration = self.get_config()

	def get_config(self) -> dict:
		load_dotenv(f"{BASE_DIR}/.env")
		host = os.getenv('DB_HOST')
		user = os.getenv('DB_USER')
		password = os.getenv('DB_PASSWORD')
		database = os.getenv('DB_NAME')
		return {'host': host,
				'user': user,
				'password': password,
				'database': database}

	def __enter__(self) -> 'cursor':
		self.conn = psycopg2.connect(**self.configuration)
		self.cursor = self.conn.cursor()
		return self.cursor

	def __exit__(self, exc_type, exc_value, exc_trace) -> None:
		self.conn.commit()
		self.cursor.close()
		self.conn.close()



if __name__ == "__main__":
	with db() as cursor:
		cursor.execute("""SELECT obj FROM app_jsonobject WHERE name=%s""", ("Вариации наименования листов", ))
		x = cursor.fetchall()[0][0]['possible_sheet_names']
		print(x)

# possible_sheet_names = JsonObject.objects.get(name="Вариации наименования листов").obj['possible_sheet_names']

