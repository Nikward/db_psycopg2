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
