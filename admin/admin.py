from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import texts
from database import *
from admin import create, setup
from instruments import settings
from trade import trade
from decimal import *
from utils.decorators import info

@info
def show_admin(_, info, bot, update, user_data):
    buy_orders = users.get_user_orders(info['tg_id'], 'crypto')
    sell_orders = users.get_user_orders(info['tg_id'], 'fiat')

    #manually add choose crypto/fiat currency buttons, buy_orders button and sell_orders button.
    keyboard = [[InlineKeyboardButton(_(texts.choose_fiat_), callback_data='settings choose_fiat from_admin'),
                InlineKeyboardButton(_(texts.choose_crypto__, callback_data='settings choose_crypto from_admin')],
                [InlineKeyboardButton(_(texts.buy_).format(len(buy_orders)), callback_data='admin my_orders buy'),
                InlineKeyboardButton(_(texts.sell_).format(len(sell_orders)), callback_data='admin my_orders sell')]
            ]

    orders = buy_orders if info['data'][2] == 'buy' else sell_orders

    for item in orders:
        visible = '' if item['visible'] else '[OFF]'
        pay_system = pay_systems.get_system_by_id(item['pay_system_id'])['name']
        symbol = item['symbol1'] if item['symbol2'] == None else item['symbol2']

        button_sign = '{} {}, {}-{}, {} {}'.format(
                                            visible,
                                            pay_system,
                                            item['alias1'], item['alias2'],
                                            item['rate'].quantize(Decimal('.01')),
                                            symbol
                                        )

        keyboard.append([InlineKeyboardButton(button_sign, callback_data='admin setup_order {}'.format(item['id']))])

    keyboard.append([InlineKeyboardButton(_(texts.back_), callback_data='trade cancel'),
                    InlineKeyboardButton(_(texts.add_), callback_data='admin create_order')])

    message = _(texts.advs_msg_).format(240000)

    info['message'].edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@info
def query_route(_, info, bot, update, user_data):
    user_data.setdefault(info['message'].message_id, { 'page' : 0 })

    if info['data'][1] == 'my_orders':
        show_admin(bot, update, user_data=user_data)
    elif info['data'][1] == 'create_order':
        return create.create_order(bot, update, user_data=user_data)
    elif info['data'][1] == 'setup_order':
        setup.setup_order(bot, update, user_data=user_data)
