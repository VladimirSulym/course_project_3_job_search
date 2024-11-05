import psycopg2


class DBManager:

    def __init__(self, name_db='hh_db'):
        self.__conn_params = {
            'host': "localhost",
            'port': 5432,
            'user': "postgres",
            'password': "qwerty123",
        }
        self.name_db = name_db
        self.__creating_database(self.name_db)
        self.__init_table()

    def __creating_database(self, name_db):
        try:
            conn = psycopg2.connect(**self.__conn_params)
            cursor = conn.cursor()
            conn.autocommit = True
            cursor.execute(f"CREATE DATABASE {name_db}")
            print("База данных успешно создана")
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)

    def __init_table(self):
        self.__conn_params['database'] = self.name_db
        with psycopg2.connect(**self.__conn_params) as conn:
            # conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("select * from information_schema.tables where table_name=%s", ('employers',))
                # print(cursor.fetchall())
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
