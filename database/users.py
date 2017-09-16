import mysql.connector
from database import connect
from datetime import datetime
import logging

logger = logging.getLogger('Main')

@connect
def register_user(cursor, data):

    query = "INSERT INTO user (tg_id, phone, username, first_name, last_name, post_stamp, lang) VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}');"
    query = query.format(
                        data['id'],
                        data.get('phone', None),
                        data.get('username', None),
                        data.get('first_name', None),
                        data.get('last_name', None),
                        datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                        'en'
                    )

    try:
        cursor.execute(query)

    except:
        logger.info('User {} {} {} with id {} already registered.'.format(data.get('username', None), data.get('last_name', None), data.get('first_name', None), data.get('id', None)))


@connect
def get_usid_by_tgid(cursor, tg_id):

    query = "SELECT id FROM user WHERE tg_id = {}".format(tg_id)

    cursor.execute(query)

    output = cursor.fetchone()

    return output[0]

@connect
def get_user_balance(cursor, tg_id):

    id_ = get_usid_by_tgid(tg_id)

    query = "SELECT balance FROM account WHERE user_id = {}".format(id_)

    cursor.execute(query)

    output = cursor.fetchone()

    return output[0]
