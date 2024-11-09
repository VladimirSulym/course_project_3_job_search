import logging

import psycopg2

from config import LOG_FORMAT, LOG_LEVEL

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(LOG_FORMAT)
logger.addHandler(console_handler)
logger.setLevel(LOG_LEVEL)

class DBManager:
    """
    Класс для подключения и работы с базой данных SQl вакансий HH
    """

    conn_params = {
        'host': "localhost",
        'port': 5432,
        'user': "postgres",
        'password': "qwerty123",
    }
    name_db = ''
    count_vacancies = 0
    count_employers = 0

    def __init__(self, name_db='hh_db'):
        self.creating_database()
        self.init_table()

    @classmethod
    def creating_database(cls, name_db='hh_db'):
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
        cls.conn_params['database'] = cls.name_db
        with psycopg2.connect(**cls.conn_params) as conn:
            # conn.autocommit = True
            with conn.cursor() as cursor:
                # проверяем, существует ли такая таблица
                cursor.execute("select * from information_schema.tables where table_name=%s", ('employers',))
                # теперь cursor содержит список с данными о запрошенной таблице
                # cursor.fetchall() - подробный список данных
                if not bool(cursor.rowcount):
                    cursor.execute("CREATE TABLE employers"
                                   "("
                                   "id int PRIMARY KEY,"
                                   "name varchar(250) NOT NULL,"
                                   "url varchar(500),"
                                   "vacancies_url varchar(500)"
                                   ")"
                                   "")
                else:
                    cursor.execute("SELECT COUNT(*) FROM employers")
                    cls.count_employers = cursor.fetchone()[0]
                    logger.info(f"Таблица employers существует и содержит {cls.count_employers} записей")


                cursor.execute("select * from information_schema.tables where table_name=%s", ('vacancies',))
                # print(cursor.fetchall())
                if not bool(cursor.rowcount):
                    cursor.execute("CREATE TABLE vacancies"
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
                                   "")
                    conn.commit()
                else:
                    cursor.execute("SELECT COUNT(*) FROM vacancies")
                    cls.count_vacancies = cursor.fetchone()[0]
                    logger.info(f"Таблица vacancies существует и содержит {cls.count_vacancies} записей")

        conn.close()

    @property
    def vacancies(self):
        return None

    @property
    def employers(self):
        return None

    @vacancies.setter
    def vacancies(self, vacancies: list):
        logger.debug(f'start => vacancies.setter')
        # DBManager.conn_params['database'] = DBManager.name_db
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                for vacancy in vacancies:
                    try:
                        cursor.execute("INSERT INTO employers VALUES (%s, %s, %s, %s)",
                                       (list(vacancy.employer.employer.values())))
                    except Exception as e:
                        print(e)
                    conn.commit()
                    try:
                        cursor.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                       (list(vacancy.vacancy.values())))
                    except Exception as e:
                        print(e)
                    conn.commit()
        conn.close()

    @employers.setter
    def employers(self, employers: list):
        logger.debug(f'start => employers.setter')
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                for employer in employers:
                    try:
                        cursor.execute("INSERT INTO employers VALUES (%s, %s, %s, %s)",
                                       (list(employer.employer.values())))
                        print('Данные сохранены в БД')
                    except Exception as e:
                        print (e.pgerror)
                        print (e.diag.message_detail)
                    conn.commit()
        conn.close()

    @staticmethod
    def get_companies_and_vacancies_count():
        """Функция получает из локальной БД список всех компаний и количество вакансий у каждой компании"""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("SELECT "
                                   "employers.name, "
                                   "COUNT(vacancies) as count FROM employers "
                                   "JOIN vacancies ON employers.id = vacancies.employer_id "
                                   "GROUP BY employers.name")
                    return cursor.fetchall()
                except Exception as e:
                    print(e)
                conn.commit()
        conn.close()

    @staticmethod
    def get_all_vacancies():
        """Функция получает из локальной БД список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("SELECT "
                                   "employers.name as name_company,"
                                   "vacancies.name as vacancy,"
                                   "salary_from,"
                                   "salary_to,"
                                   "vacancies.url "
                                   "FROM vacancies "
                                   "JOIN employers ON employers.id = vacancies.employer_id")
                    return cursor.fetchall()
                except Exception as e:
                    print(e)
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
                    print(e)
                conn.commit()
        conn.close()


    @staticmethod
    def get_vacancies_with_higher_salary():
        """Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("SELECT "
                                   "id, "
                                   "name, "
                                   "salary_from, "
                                   "salary_to, "
                                   "url "
                                   "FROM vacancies "
                                   "WHERE salary_from > (SELECT AVG(salary_from) from vacancies)")
                    return cursor.fetchall()
                except Exception as e:
                    print(e)
                conn.commit()
        conn.close()


    @staticmethod
    def get_vacancies_with_keyword(search_str):
        """Функция получает список всех вакансий из локальной БД, в названии которых содержатся
        переданные в метод слова, например python."""
        with psycopg2.connect(**DBManager.conn_params) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(f"SELECT "
                                   f"id, "
                                   f"name, "
                                   f"salary_from, "
                                   f"salary_to, "
                                   f"url FROM vacancies WHERE name LIKE '%{search_str}%'")
                    return cursor.fetchall()
                except Exception as e:
                    print(e)
                conn.commit()
        conn.close()


if __name__ == '__main__':
    db_manager = DBManager()
    print(db_manager.get_vacancies_with_keyword('python'))

    # with connect_db() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute('CREATE TABLE user_account'
    #                     '('
    #                     'user_id int PRIMARY KEY,'
    #                     'fullname varchar(100) NOT NULL,'
    #                     'address varchar(300) DEFAULT \'Moscow\''
    #                     ')')
    # conn.close()
