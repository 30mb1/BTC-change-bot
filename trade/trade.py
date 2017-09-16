from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from trade import exchange
from trade import orders

MENU, WITHDRAW = range(2)


def show_trade(bot, update):
    message = texts.trade_msg_.format(240000) + 'RUB'

    keyboard = [
        [InlineKeyboardButton("Buy 📈", callback_data='trade buy'),
        InlineKeyboardButton("Sell 📉", callback_data='trade sell'),
        InlineKeyboardButton(texts.my_advs_, callback_data='trade advs')]
    ]

    if update.callback_query:
        update.callback_query.message.edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        return
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
        exchange.show_orders(bot, update, user_data)
    elif data == 'next_orders' or data == 'back_systems':
        exchange.show_orders(bot, update, user_data)
    elif data == 'advs':
        advertisements.show_orders(bot, update, user_data)
    elif data == 'create':
        orders.create_order(bot, update, user_data)
    elif data == 'cancel':
        user_data.clear()
        show_trade(bot, update)
