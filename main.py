import configparser
import os.path

import psycopg2


def get_database_info():
    config = configparser.ConfigParser()
    path = os.path.dirname(__file__) + '\setting.ini'
    config.read(path)
    name_db = config['database_info']['database']
    user = config['database_info']['user']
    password = config['database_info']['password']
    return name_db, user, password


def create_db(curs):
    curs.execute("""
    CREATE TABLE IF NOT EXISTS staffs(
        id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        lastname VARCHAR(30),
        email VARCHAR(100)
        );
    """)
    curs.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
        number VARCHAR(11) PRIMARY KEY,
        staff_id INTEGER REFERENCES staffs(id)
        );
    """)

    def delete_tables(curs):
        curs.execute("""
            DROP TABLE staffs, phonenumbers CASCADE;
            """)


if __name__ == '__main__':
    with psycopg2.connect(database=get_database_info()[0], user=get_database_info()[1],
                          password=get_database_info()[2]) as conn:
        pass  # вызывайте функции здесь
