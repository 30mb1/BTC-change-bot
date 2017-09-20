from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from database import users, pay_systems
from decimal import *

def show_order(bot, update, user_data):
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data.split()

    order_id = data[2]

    order = pay_systems.get_order_by_id(order_id)

    user = users.get_user_by_usid(order['user_id'])

    pay_system = pay_systems.get_system_by_id(order['pay_system_id'])

    crypto_cur = pay_systems.get_currency_by_id(user['base_currency_id'])

    fiat_cur = pay_systems.get_currency_by_id(user['base_fiat_currency_id'])

    user_currency_id = users.get_user_by_tgid(update.callback_query.from_user.id)['base_currency_id']
    user_currency = pay_systems.get_currency_by_id(user_currency_id)

    if user_data[msg_id]['trade'] == 'buy':
        message = texts.buy_order_
    else:
        message = texts.sell_order_

    message = message.format(
            user_currency['name'],
            pay_system['name'],
            user['username'],
            order['message'],
            crypto_cur['alias'],
            order['rate'].quantize(Decimal('.01')),
            fiat_cur['alias'],
            order['min'].quantize(Decimal('.01')),
            fiat_cur['alias'],
            order['max'].quantize(Decimal('.01')),
            fiat_cur['alias']
        )

    keyboard = [[InlineKeyboardButton(texts.cancel_, callback_data='trade system {}'.format(order['pay_system_id'])), InlineKeyboardButton(texts.start_deal_, callback_data='trade start_deal {}'.format(order_id))]]

    update.callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
