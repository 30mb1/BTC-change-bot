import mysql.connector
from database import connect, users, pay_systems
from datetime import datetime
import logging

logger = logging.getLogger('Main')


@connect
def create_order(cursor, user_id, order_info, **kwargs):
    pay_system_id = pay_systems.get_system_by_name(order_info['pay_system'])['id']

    query = ("INSERT INTO `order` (user_id, base_currency_id, ref_currency_id, rate,"
    " min, max, message, pay_system_id, visible) VALUES ('{}', '{}', '{}', '{}', '{}', '{"
    "}', '{}', '{}', '{}');")

    query = query.format(
                        user_id,
                        order_info['base_currency_id'],
                        order_info['ref_currency_id'],
                        order_info['rate'],
                        240000,
                        250000,
                        order_info['message'],
                        pay_system_id,
                        1
                    )

    cursor.execute(query)
