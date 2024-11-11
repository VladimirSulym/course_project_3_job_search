import logging
import os

import psycopg2
from dotenv import load_dotenv

from config import LOG_FORMAT, LOG_LEVEL

load_dotenv()

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(LOG_FORMAT)
logger.addHandler(console_handler)
logger.setLevel(LOG_LEVEL)


class DBInit:
    """Класс для подключения к локальной базе данных вакансий HH, создания БД и создания основных таблиц"""

    conn_params = {
        "host": os.getenv("DATABASE_HOST"),
        "port": os.getenv("DATABASE_PORT"),
        "user": os.getenv("DATABASE_USER"),
        "password": os.getenv("DATABASE_PASSWORD"),
    }
    name_db = ""
    count_vacancies = 0
    count_employers = 0

    def __init__(self, name_db="hh_db"):
        self.creating_database()
        self.init_table()

    @classmethod
    def creating_database(cls, name_db="hh_db"):
        """
        Функция создает базу данных на сервере SQL
        """
        try:
            cls.name_db = name_db
            conn = psycopg2.connect(**cls.conn_params)
            cursor = conn.cursor()
            conn.autocommit = True  # Благодаря этому команда SQL, Во-первых, выполняется немедленно.
            # А во-вторых, выполняется вне транзакции
            # (выражение "CREATE DATABASE" должно выполняться именно вне транзакции)
            cursor.execute(f"CREATE DATABASE {name_db}")
            print(f"База данных {name_db} успешно создана")
            cursor.close()
            conn.close()
        except Exception as e:
            logger.info(e)

    @classmethod
    def init_table(cls):
        """
        Функция создает основные таблицы в базе данных которую создал данный класс
        """
        cls.conn_params["database"] = cls.name_db
        with psycopg2.connect(**cls.conn_params) as conn:
            # conn.autocommit = True
            with conn.cursor() as cursor:
                # проверяем, существует ли такая таблица
                # cursor.execute("select * from information_schema.tables where table_name=%s", ('employers',))
                # теперь cursor содержит список с данными о запрошенной таблице
                # cursor.fetchall() - подробный список данных
                # if not bool(cursor.rowcount):
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS employers"
                    "("
                    "id int PRIMARY KEY,"
                    "name varchar(250) NOT NULL,"
                    "url varchar(500),"
                    "vacancies_url varchar(500)"
                    ")"
                    ""
                )
                # else:
                cursor.execute("SELECT COUNT(*) FROM employers")
                cls.count_employers = cursor.fetchone()[0]
                logger.info(f"Таблица employers содержит {cls.count_employers} записей")

                # cursor.execute("select * from information_schema.tables where table_name=%s", ('vacancies',))
                # print(cursor.fetchall())
                # if not bool(cursor.rowcount):
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS vacancies"
                    "("
                    "id int PRIMARY KEY,"
                    "name varchar(250) NOT NULL,"
                    "employer_id int NOT NULL REFERENCES employers(id),"
                    "area varchar(100),"
                    "salary_from int,"
                    "salary_to int,"
                    "currency varchar(5),"
                    "url varchar(500),"
                    "requirement text,"
                    "responsibility text,"
                    "schedule varchar(250)"
                    ")"
                    ""
                )
                conn.commit()
                # else:
                cursor.execute("SELECT COUNT(*) FROM vacancies")
                cls.count_vacancies = cursor.fetchone()[0]
                logger.info(f"Таблица vacancies содержит {cls.count_vacancies} записей")

        conn.close()
