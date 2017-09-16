import mysql.connector
from database import connect
from datetime import datetime
import logging
from database import users

@connect
def get_pay_systems_list(cursor, tg_id):
    user = users.get_user_by_tgid(tg_id)

    query = "SELECT name, id FROM pay_system WHERE currency_id = {};".format(user['base_fiat_currency_id'])

    cursor.execute(query)

    systems_list = cursor.fetchall()

    return [{'name' : i[0], 'id' : i[1]} for i in systems_list]

@connect
def get_system_name_by_id(cursor, id_):
    query = "SELECT name FROM pay_system WHERE id = {};".format(id_)

    cursor.execute(query)

    return cursor.fetchone()[0]

@connect
def get_orders_for_system(cursor, tg_id, buy, system_id):
    user = users.get_user_by_tgid(tg_id)

    reverse = ''
    if buy:
        base, ref = user['base_fiat_currency_id'], user['base_currency_id']
    else:
        base, ref = user['base_currency_id'], user['base_fiat_currency_id']
        reverse = 'DESC'

    query = "SELECT * FROM `order` WHERE base_currency_id = {} AND ref_currency_id = {} AND pay_system_id = {} ORDER BY rate {};".format(base, ref, system_id, reverse)

    print (query)

    cursor.execute(query)

    orders_list = cursor.fetchall()

    return [{'user_id' : i[1], 'rate' : i[4], 'min' : i[5], 'max' : i[6], 'message' : i[7]} for i in orders_list]
