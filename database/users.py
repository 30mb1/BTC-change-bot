import mysql.connector
from database import connect
from datetime import datetime
import logging

logger = logging.getLogger('Main')

@connect
def register_user(cursor, data):

    query = "INSERT INTO user (tg_id, phone, username, first_name, last_name, post_stamp, lang, base_fiat_currency_id, base_currency_id) VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}');"
    query = query.format(
                        data['id'],
                        data.get('phone', None),
                        data.get('username', None),
                        data.get('first_name', None),
                        data.get('last_name', None),
                        datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                        'en',
                        2,
                        1
                    )

    try:
        cursor.execute(query)

    except:
        logger.info('User {} {} {} with id {} already registered.'.format(data.get('username', None), data.get('last_name', None), data.get('first_name', None), data.get('id', None)))


@connect
def get_user_by_tgid(cursor, tg_id):

    query = "SELECT * FROM user WHERE tg_id = {}".format(tg_id)

    cursor.execute(query)

    out = cursor.fetchone()

    return {'id' : out[0], 'phone' : out[2], 'username' : out[3], 'first_name' : out[4], 'last_name' : out[5], 'lang' : out[6], 'base_fiat_currency_id' : out[8], 'base_currency_id' : out[9]}

@connect
def get_user_by_usid(cursor, user_id):
    query = "SELECT * FROM user WHERE id = {}".format(user_id)

    cursor.execute(query)

    out = cursor.fetchone()

    return {'id' : out[0], 'phone' : out[2], 'username' : out[3], 'first_name' : out[4], 'last_name' : out[5], 'lang' : out[6], 'base_fiat_currency_id' : out[8], 'base_currency_id' : out[9]}

@connect
def get_user_balance(cursor, tg_id):

    user = get_user_by_tgid(tg_id)

    query = "SELECT balance FROM account WHERE user_id = {}".format(user['id'])

    cursor.execute(query)

    output = cursor.fetchone()

    return output[0]

@connect
def get_user_orders(cursor, tg_id, type_):
    user = get_user_by_tgid(tg_id)

    #select only rows when we buy crypt currencies
    query = ("SELECT t1.visible, t1.pay_system_id, t1.rate, t2.alias, t3.symbol, t1.id, t2.symbol, t3.alias\n"
            "FROM `order` t1\n"
            "CROSS JOIN `currency` t2 ON t1.ref_currency_id = t2.id AND t2.type = '{}'\n"
            "CROSS JOIN `currency` t3 ON t3.id = t1.base_currency_id\n"
            "WHERE t1.user_id = {}".format(type_, user['id']))

    cursor.execute(query)

    orders_list = cursor.fetchall()

    return [{ 'visible' : order[0], 'pay_system_id' : order[1], 'rate' : order[2], 'alias1' : order[3], 'symbol1' : order[4], 'symbol2' : order[6], 'id' : order[5], 'alias2' : order[7] } for order in orders_list]

@connect
def set_currency(cursor, tg_id, currency_id, type_):
    if type_ == 'fiat':
        query = "UPDATE user SET base_fiat_currency_id = {} WHERE tg_id = {}".format(currency_id, tg_id)
    else:
        query = "UPDATE user SET base_currency_id = {} WHERE tg_id = {}".format(currency_id, tg_id)

    cursor.execute(query)
