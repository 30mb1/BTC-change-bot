from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from database import users, pay_systems
from admin import create, settings
from trade import trade
from decimal import *

def show_admin(bot, update, user_data):
    tg_id = update.callback_query.from_user.id
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data.split()

    message = texts.advs_msg_.format(240000)

    buy_orders = users.get_user_buy_orders(tg_id)
    sell_orders =  users.get_user_sell_orders(tg_id)

    #manually add add_new_order button, buy_orders button and sell_orders button.
    keyboard = [[InlineKeyboardButton(texts.choose_fiat_, callback_data='admin choose_fiat'),
                InlineKeyboardButton(texts.choose_crypto_, callback_data='admin choose_crypto')],
                [InlineKeyboardButton(texts.buy_.format(len(buy_orders)), callback_data='admin my_orders buy'),
                InlineKeyboardButton(texts.sell_.format(len(sell_orders)), callback_data='admin my_orders sell')]
            ]

    orders = buy_orders if data[2] == 'buy' else sell_orders

    for item in orders:
        visible = '' if item['visible'] else '[OFF]'
        pay_system = pay_systems.get_system_by_id(item['pay_system_id'])['name']
        button_sign = '{} {}, {}, {}, {}'.format(
                                            visible,
                                            pay_system,
                                            item['alias'],
                                            item['rate'].quantize(Decimal('.01')),
                                            item['symbol']
                                        )

        keyboard.append([InlineKeyboardButton(button_sign, callback_data='admin setup_order {}'.format(item['id']))])

    keyboard.append([InlineKeyboardButton(texts.back_, callback_data='trade cancel'), InlineKeyboardButton(texts.add_, callback_data='admin create_order')])

    update.callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

def query_route(bot, update, user_data):
    query = update.callback_query
    data = query.data.split()[1]

    user_data.setdefault(query.message.message_id, { 'page' : 0 })

    if data == 'my_orders':
        show_admin(bot, update, user_data)
    elif data == 'cancel':
        trade.show_trade(bot, update)
    elif data == 'create_order':
        create.create_order(bot, update, user_data)
    elif data == 'choose_fiat':
        settings.set_fiat(bot, update, user_data)
    elif data == 'choose_crypto':
        settings.set_crypto(bot, update, user_data)
    elif data == 'setup_order':
        settings.setup__order(bot, update, user_data)
