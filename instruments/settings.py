from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from database import users, pay_systems
from admin import create, setup, admin
from instruments import instruments
from trade import trade
from decimal import *

ROW_SIZE = 4

@info
def set_currency(info, bot, update, user_data):
    #get currency type from set_crypto/set_fiat string in data
    users.set_currency(info['tg_id'], info['data'][2], info['data'][1][4:])
    if info['data'][3] == 'from_admin':
        admin.show_admin(bot, update, user_data)
    else:
        instruments.show_instruments(bot, update, user_data)

@info
def choose_currency(info, bot, update, user_data):
    #get currency type from choose_fiat/choose_crypto string in data
    cur_type = info['data'][1][7:]

    fiat_list = pay_systems.get_currencies_of_type(cur_type)

    fiat_row_list = [fiat_list[i:i + ROW_SIZE] for i in range(0, len(fiat_list), ROW_SIZE)]

    keyboard = []

    for row in fiat_row_list:
        button_row = []
        for cur in row:
            button_row.append(InlineKeyboardButton(cur['alias'], callback_data='settings set_{} {} {}'.format(cur_type, cur['id'], info['data'][2])))
        keyboard.append(button_row)

    if info['data'][2] == 'from_admin':
        keyboard.append([InlineKeyboardButton(texts.back_, callback_data='admin my_orders buy')])
    else:
        keyboard.append([InlineKeyboardButton(texts.back_, callback_data='settings cancel')])

    message = texts.fiat_msg_ if cur_type == 'fiat' else texts.crypto_msg

    info['message'].edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
