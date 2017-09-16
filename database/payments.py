import mysql.connector
from database import connect
from datetime import datetime
import logging
from database import users

logger = logging.getLogger('Main')

@connect
def withdraw_money(cursor, tg_id, amount):
    id_ = users.get_usid_by_tgid(tg_id)

    query = "UPDATE account SET balance = balance - {} WHERE id = {} AND balance >= {};".format(amount, id_, amount)

    cursor.execute(query)

    #user have enough funds, row was updated
    if cursor.rowcount:
        return True

    return False
