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
    return "БАЗА ДАННЫХ СОЗДАНА"


def delete_tables(curs):
    curs.execute("""
        DROP TABLE staffs, phonenumbers CASCADE;
        """)


def insert_number(curs, staff_id, number):
    curs.execute("""
            INSERT INTO phonenumbers(number, staff_id)
            VALUES (%s, %s)
            """, (number, staff_id))
    return f'Добавлен телефон {number} пользователя {staff_id}'


def insert_staff(curs, name=None, surname=None, email=None, number=None):
    curs.execute("""
        INSERT INTO staffs(name, lastname, email)
        VALUES (%s, %s, %s)
        """, (name, surname, email))
    curs.execute("""
        SELECT id from staffs
        ORDER BY id DESC
        LIMIT 1
        """)
    id = curs.fetchone()[0]
    if number is None:
        return f'Добавлен клиент {id}'
    else:
        insert_number(curs, id, number)
        return id


def update_staff(curs, id, name=None, surname=None, email=None):
    curs.execute("""
        SELECT * from staffs
        WHERE id = %s
        """, (id,))
    info = curs.fetchone()
    if name is None:
        name = info[1]
    if surname is None:
        surname = info[2]
    if email is None:
        email = info[3]
    curs.execute("""
        UPDATE staffs
        SET name = %s, lastname = %s, email =%s 
        where id = %s
        """, (name, surname, email, id))
    return f'Клиент с id {id} изменен'


def delete_phone(curs, number):
    curs.execute("""
        DELETE FROM phonenumbers 
        WHERE number = %s
        """, (number,))
    return f'{number} удален'


def delete_staff(curs, id):
    curs.execute("""
        DELETE FROM phonenumbers
        WHERE staff_id = %s
        """, (id,))
    curs.execute("""
        DELETE FROM staffs 
        WHERE id = %s
       """, (id,))
    return f'Клиент с id {id} удален'


def find_sraff(curs, name=None, surname=None, email=None, tel=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if tel is None:
        curs.execute("""
            SELECT s.id, s.name, s.lastname, s.email, p.number FROM staffs s
            LEFT JOIN phonenumbers p ON s.id = p.staff_id
            WHERE s.name LIKE %s AND s.lastname LIKE %s
            AND s.email LIKE %s
            """, (name, surname, email))
    else:
        curs.execute("""
            SELECT s.id, s.name, s.lastname, s.email, p.number FROM staffs s
            LEFT JOIN phonenumbers p ON s.id = p.staff_id
            WHERE s.name LIKE %s AND s.lastname LIKE %s
            AND s.email LIKE %s AND p.number like %s
            """, (name, surname, email, tel))
    return curs.fetchall()


if __name__ == '__main__':
    with psycopg2.connect(database=get_database_info()[0], user=get_database_info()[1],
                          password=get_database_info()[2]) as conn:
        with conn.cursor() as curs:
            delete_tables(curs)
            print(create_db(curs))
            print(insert_staff(curs, "Михаил", "Шабалин", "71113111108@gmail.com"))
            print(insert_staff(curs, "Максим", "Смирнов", "71222222@gmail.com"))
            print(insert_staff(curs, "Михаил", "Литвин", "7152211@gmail.com"))
            print(insert_staff(curs, "Вася", "Пупкин", "732322@gmail.com"))
            print(insert_number(curs, 2, 89103332432))
            print(insert_number(curs, 3, 89103222432))
            print(update_staff(curs, 4, "Леня", None, '123@outlook.com'))
            print(delete_phone(curs, '89103222432'))
            print(delete_staff(curs, 2))
            print(find_sraff(curs, 'Михаил'))
