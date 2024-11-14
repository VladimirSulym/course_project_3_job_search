import logging

import psycopg2

from config import LOG_FORMAT, LOG_LEVEL
from src.db_init import DBInit

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(LOG_FORMAT)
logger.addHandler(console_handler)
logger.setLevel(LOG_LEVEL)


class DBManager(DBInit):
    """
    Класс для работы с базой данных SQl вакансий HH
    """

    @property
    def vacancies(self):
        return None

    @property
    def employers(self):
        return None

    @vacancies.setter
    def vacancies(self, vacancies: list):
        """Функция для внесения вакансии в БД"""
        logger.debug("start => vacancies.setter")
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                for vacancy in vacancies:
                    try:
                        cursor.execute(
                            "INSERT INTO employers VALUES (%s, %s, %s, %s)", (list(vacancy.employer.employer.values()))
                        )
                    except Exception as e:
                        logger.debug(e)
                    conn.commit()
                    try:
                        cursor.execute(
                            "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (list(vacancy.vacancy.values())),
                        )
                        print("Вакансия сохранена в БД")
                    except Exception as e:
                        print("Вакансия уже существует в БД")
                        logger.debug(e)
                    conn.commit()
        conn.close()

    @employers.setter
    def employers(self, employers: list):
        """Функция для внесения работодателей в БД"""
        logger.debug("start => employers.setter")
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                for employer in employers:
                    try:
                        cursor.execute(
                            "INSERT INTO employers VALUES (%s, %s, %s, %s)", (list(employer.employer.values()))
                        )
                        print("Работодатель сохранен в БД")
                    except Exception as e:
                        print("Работодатель уже существует в БД")
                        logger.debug(e)
                    conn.commit()
        conn.close()

    @staticmethod
    def get_companies_and_vacancies_count():
        """Функция получает из локальной БД список всех компаний и количество вакансий у каждой компании"""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "SELECT "
                        "employers.id, "
                        "employers.name, "
                        "COUNT(vacancies) as count FROM employers "
                        "JOIN vacancies ON employers.id = vacancies.employer_id "
                        "GROUP BY employers.id"
                    )
                    return cursor.fetchall()
                except Exception as e:
                    logger.debug(e)
                conn.commit()
        conn.close()

    @staticmethod
    def get_all_vacancies():
        """Функция получает из локальной БД список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "SELECT "
                        "employers.name as name_company,"
                        "vacancies.name as vacancy,"
                        "salary_from,"
                        "salary_to,"
                        "vacancies.url "
                        "FROM vacancies "
                        "JOIN employers ON employers.id = vacancies.employer_id"
                    )
                    return cursor.fetchall()
                except Exception as e:
                    logger.debug(e)
                conn.commit()
        conn.close()

    @staticmethod
    def get_avg_salary():
        """Функция получает из локальной БД среднюю зарплату по вакансиям."""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("SELECT AVG(salary_from) FROM vacancies")
                    return round(cursor.fetchall()[0][0], 2)
                except Exception as e:
                    logger.debug(e)
                conn.commit()
        conn.close()

    @staticmethod
    def get_vacancies_with_higher_salary():
        """Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        "SELECT "
                        "id, "
                        "name, "
                        "salary_from, "
                        "salary_to, "
                        "url "
                        "FROM vacancies "
                        "WHERE salary_from > (SELECT AVG(salary_from) from vacancies)"
                    )
                    return cursor.fetchall()
                except Exception as e:
                    logger.debug(e)
                conn.commit()
        conn.close()

    @staticmethod
    def get_vacancies_with_keyword(search_str):
        """Функция получает список всех вакансий из локальной БД, в названии которых содержатся
        переданные в функцию слова."""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        f"SELECT "
                        f"id, "
                        f"name, "
                        f"salary_from, "
                        f"salary_to, "
                        f"url "
                        f"FROM vacancies "
                        f"WHERE name ILIKE '%{search_str}%' "
                        f"OR requirement ILIKE '%{search_str}%' "
                        f"OR responsibility ILIKE '%{search_str}%'"
                    )
                    return cursor.fetchall()
                except Exception as e:
                    logger.debug(e)
                conn.commit()
        conn.close()
