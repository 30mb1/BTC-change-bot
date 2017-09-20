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
def get_system_by_id(cursor, id_):
    query = "SELECT * FROM pay_system WHERE id = {};".format(id_)

    cursor.execute(query)

    res = cursor.fetchone()

    return { 'id' : res[0], 'name' : res[1], 'currency_id' : res[2] }

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

    cursor.execute(query)

    orders_list = cursor.fetchall()

    return [{'id' : i[0], 'user_id' : i[1], 'rate' : i[4], 'min' : i[5], 'max' : i[6], 'message' : i[7]} for i in orders_list]

@connect
def get_currency_by_id(cursor, cur_id):
    query = "SELECT * FROM currency WHERE id = {};".format(cur_id)

    cursor.execute(query)

    res = cursor.fetchone()

    return { 'id' : res[0], 'type' : res[1], 'symbol' : res[2], 'name' : res[3], 'alias' : res[4], 'description' : res[5] }

@connect
def get_order_by_id(cursor, order_id):
    query = "SELECT * FROM `order` WHERE id = {};".format(order_id)

    cursor.execute(query)

    res = cursor.fetchone()

    return { 'id' : res[0], 'user_id' : res[1], 'base_currency_id' : res[2], 'ref_currency_id' : res[3], 'rate' : res[4], 'min' : res[5], 'max' : res[6], 'message' : res[7], 'pay_system_id' : res[8], 'visible' : res[9] }

@connect
def get_currencies_of_type(cursor, type_):
    query = "SELECT * FROM currency WHERE type ='{}'".format(type_)

    cursor.execute(query)

    currency_list = cursor.fetchall()

    return [{ 'id' : cur[0], 'alias' : cur[4] } for cur in currency_list]
