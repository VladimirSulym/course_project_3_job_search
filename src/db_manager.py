import psycopg2


class DBManager:
    """
    Класс для подключения и работы с базой данных SQl вакансий HH
    """

    def __init__(self, name_db='hh_db'):
        self.__conn_params = {
            'host': "localhost",
            'port': 5432,
            'user': "postgres",
            'password': "qwerty123",
        }
        self.name_db = name_db
        self.__creating_database()
        self.__init_table()
        self.__count_vacancies = 0
        self.__count_employers = 0

    def __creating_database(self):
        """
        Функция создает базу данных на сервере SQL
        """
        try:
            conn = psycopg2.connect(**self.__conn_params)
            cursor = conn.cursor()
            conn.autocommit = True  # Благодаря этому команда SQL, Во-первых, выполняется немедленно.
            # А во-вторых, выполняется вне транзакции
            # (выражение "CREATE DATABASE" должно выполняться именно вне транзакции)
            cursor.execute(f"CREATE DATABASE {self.name_db}")
            print(f"База данных {self.name_db} успешно создана")
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)

    def __init_table(self):
        """
        Функция создает основные таблицы в базе данных которую создал данный класс
        """
        self.__conn_params['database'] = self.name_db
        with psycopg2.connect(**self.__conn_params) as conn:
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
                    self.__count_employers = cursor.fetchone()[0]
                    print(self.__count_employers)
                    print("Таблица employers существует")


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
                    self.__count_vacancies = cursor.fetchone()[0]
                    print(self.__count_vacancies)
                    print("Таблица vacancies существует")
        conn.close()

    @property
    def vacancies(self):
        return None

    @vacancies.setter
    def vacancies(self, vacancies: list):
        print('запущен сетер')
        self.__conn_params['database'] = self.name_db
        with psycopg2.connect(**self.__conn_params) as conn:
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


# get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.
# get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
# get_avg_salary() — получает среднюю зарплату по вакансиям.
# get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
# get_vacancies_with_keyword() — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.

if __name__ == '__main__':
    DBManager()

    # with connect_db() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute('CREATE TABLE user_account'
    #                     '('
    #                     'user_id int PRIMARY KEY,'
    #                     'fullname varchar(100) NOT NULL,'
    #                     'address varchar(300) DEFAULT \'Moscow\''
    #                     ')')
    # conn.close()
