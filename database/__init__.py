import mysql.connector
from configparser import ConfigParser

__all__ = ["pay_systems", "payments", "users"]


parser = ConfigParser()
parser.read('config.ini')


def connect(func):
    def wrapper(*args, **kwargs):
        cnx = mysql.connector.connect(user=parser.get('DATABASE', 'user'), database=parser.get('DATABASE', 'name'), password=parser.get('DATABASE', 'password'))
        cursor = cnx.cursor()
        res = func(cursor, *args, **kwargs)
        cnx.commit()
        cursor.close()
        cnx.close()

        return res

    return wrapper
