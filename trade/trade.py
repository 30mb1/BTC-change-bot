from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from trade import exchange, orders
from admin import admin
from database import pay_systems, users

MENU, WITHDRAW = range(2)

def show_trade(bot, update):
    keyboard = [
        [InlineKeyboardButton("Buy 📈", callback_data='trade buy'),
        InlineKeyboardButton("Sell 📉", callback_data='trade sell'),
        InlineKeyboardButton(texts.my_advs_, callback_data='admin my_orders buy')]
    ]

    if update.callback_query:

        currency_id = users.get_user_by_tgid(update.callback_query.from_user.id)['base_currency_id']
        currency = pay_systems.get_currency_by_id(currency_id)

        message = texts.trade_msg_.format(currency['name'], currency['name'], 240000) + 'RUB'

        update.callback_query.message.edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    currency_id = users.get_user_by_tgid(update.message.from_user.id)['base_currency_id']
    currency = pay_systems.get_currency_by_id(currency_id)

    message = texts.trade_msg_.format(currency['name'], currency['name'], 240000) + 'RUB'

    update.message.reply_text(message,  reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN)

def query_route(bot, update, user_data):
    query = update.callback_query
    data = query.data.split()[1]

    user_data.setdefault(query.message.message_id, { 'page' : 0 })

    if data == 'buy' or data == 'sell':
        user_data[query.message.message_id]['trade'] = data
        exchange.show_pay_systems(bot, update, user_data)
    elif data == 'next_systems' or data == 'back_systems':
        exchange.show_pay_systems(bot, update, user_data)
    elif data == 'system':
        user_data[query.message.message_id]['page'] = 0
        exchange.show_system_orders(bot, update, user_data)
    elif data == 'next_orders' or data == 'back_orders':
        exchange.show_system_orders(bot, update, user_data)
    elif data == 'show_order':
        orders.show_order(bot, update, user_data)
    elif data == 'cancel':
        user_data.pop(query.message.message_id, None)
        show_trade(bot, update)
