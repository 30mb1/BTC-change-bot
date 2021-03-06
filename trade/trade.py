from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import texts
from trade import exchange, orders
from database import *
from utils.decorators import info

MENU, WITHDRAW, CHOOSE_TYPE, PAY_SYSTEM, RATE, LIMMITS = range(6)

@info
def show_trade(_, info, bot, update, user_data):
    keyboard = [
        [InlineKeyboardButton(_(texts.buy_button_), callback_data='trade buy'),
        InlineKeyboardButton(_(texts.sell_button_), callback_data='trade sell'),
        InlineKeyboardButton(_(texts.my_advs_), callback_data='admin my_orders buy')]
    ]

    currency_id = users.get_user_by_tgid(info['tg_id'])['base_currency_id']
    currency = pay_systems.get_currency_by_id(currency_id)

    message = _(texts.trade_msg_).format(currency['name'], currency['name'], 240000) + 'RUB'

    if info['callback']:

        info['message'].edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    info['message'].reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

#determine what to do using callback data
@info
def query_route(_, info, bot, update, user_data):
    user_data.setdefault(info['message'].message_id, { 'page' : 0 })

    if info['data'][1] == 'buy' or info['data'][1] == 'sell':
        user_data[info['message'].message_id]['page'] = 0
        user_data[info['message'].message_id]['trade'] = info['data'][1]
        exchange.show_pay_systems(bot, update, user_data=user_data)

    elif info['data'][1] == 'next_systems' or info['data'][1] == 'back_systems':
        exchange.show_pay_systems(bot, update, user_data=user_data)

    elif info['data'][1] == 'system':
        user_data[info['message'].message_id]['page'] = 0
        exchange.show_system_orders(bot, update, user_data=user_data)

    elif info['data'][1] == 'next_orders' or info['data'][1] == 'back_orders':
        exchange.show_system_orders(bot, update, user_data=user_data)

    elif info['data'][1] == 'show_order':
        orders.show_order(bot, update, user_data=user_data)

    elif info['data'][1] == 'cancel':
        user_data.pop(info['message'].message_id, None)
        show_trade(bot, update, user_data=user_data)
