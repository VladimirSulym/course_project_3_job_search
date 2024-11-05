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

    def __creating_database(self):
        """
        Функция создает базу данных на сервере SQL
        """
        try:
            conn = psycopg2.connect(**self.__conn_params)
            cursor = conn.cursor()
            conn.autocommit = True # Благодаря этому команда SQL, Во-первых, выполняется немедленно.
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
                                   "url varchar(500)"
                                   ")"
                                   "")
                else:
                    print("Таблица employers существует")

                cursor.execute("select * from information_schema.tables where table_name=%s", ('vacancies',))
                # print(cursor.fetchall())
                if not bool(cursor.rowcount):
                    cursor.execute("CREATE TABLE vacancies"
                                   "("
                                   "id int PRIMARY KEY,"
                                   "name varchar(250) NOT NULL,"
                                   "area varchar(100),"
                                   "salary_from int,"
                                   "salary_to int,"
                                   "currency varchar(5),"
                                   "url varchar(500),"
                                   "employer_id int NOT NULL REFERENCES employers(id)"
                                   ")"
                                   "")
                    conn.commit()
                else:
                    print("Таблица vacancies существует")
        conn.close()


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
