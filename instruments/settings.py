from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from database import users, pay_systems
from admin import create, setup, admin
from instruments import instruments
from trade import trade
from decimal import *

ROW_SIZE = 4

def set_currency(bot, update, user_data):
    data = update.callback_query.data.split()
    tg_id = update.callback_query.from_user.id

    #get currency type from set_crypto/set_fiat string in data
    users.set_currency(tg_id, data[2], data[1][4:])
    if data[3] == 'from_admin':
        admin.show_admin(bot, update, user_data)
    else:
        instruments.show_instruments(bot, update, user_data)

def choose_currency(bot, update, user_data):
    data = update.callback_query.data.split()
    tg_id = update.callback_query.from_user.id

    #get currency type from choose_fiat/choose_crypto string in data
    cur_type = data[1][7:]

    fiat_list = pay_systems.get_currencies_of_type(cur_type)

    fiat_row_list = [fiat_list[i:i + ROW_SIZE] for i in range(0, len(fiat_list), ROW_SIZE)]

    keyboard = []

    for row in fiat_row_list:
        button_row = []
        for cur in row:
            button_row.append(InlineKeyboardButton(cur['alias'], callback_data='settings set_{} {} {}'.format(cur_type, cur['id'], data[2])))
        keyboard.append(button_row)

    if data[2] == 'from_admin':
        keyboard.append([InlineKeyboardButton(texts.back_, callback_data='admin my_orders buy')])
    else:
        keyboard.append([InlineKeyboardButton(texts.back_, callback_data='settings cancel')])

    message = texts.fiat_msg_ if cur_type == 'fiat' else texts.crypto_msg

    update.callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )
