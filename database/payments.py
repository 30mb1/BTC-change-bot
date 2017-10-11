import mysql.connector
from database import connect
from datetime import datetime
import logging
from database import users

logger = logging.getLogger('Main')

@connect
def withdraw_money(cursor, tg_id, amount):
    user = users.get_user_by_tgid(tg_id)
    query = "UPDATE account SET balance = balance - {} WHERE user_id = {} AND balance >= {} AND currency_id = {};".format(
                                                                                                                        amount,
                                                                                                                        user['id'],
                                                                                                                        amount,
                                                                                                                        user['base_currency_id']
                                                                                                                    )

    cursor.execute(query)

    #user have enough funds, row was updated
    if cursor.rowcount:
        return True

    return False
