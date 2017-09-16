from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from trade import listing
from trade import advertisements

MENU, WITHDRAW = range(2)


def show_trade(bot, update):
    message = texts.trade_msg_.format(9999999) + 'RUB'

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
        listing.show_pay_systems(bot, update, user_data)
    elif data == 'next_systems' or data == 'back_systems':
        listing.show_pay_systems(bot, update, user_data)
    elif data == 'cancel':
        user_data[query.message.message_id]['page'] = 0
        show_trade(bot, update)
    elif data == 'advs':
        advertisements.show_advertisements(bot, update, user_data)
    elif data == 'create':
        advertisements.create_advertisement(bot, update, user_data)
