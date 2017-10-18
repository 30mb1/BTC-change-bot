from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import texts
from database import *
from decimal import *
from utils.decorators import info

@info
def show_order(_, info, bot, update, user_data):
    order_id = info['data'][2]

    # get all info about this order
    order = pay_systems.get_order_by_id(order_id)

    user = users.get_user_by_usid(order['user_id'])

    pay_system = pay_systems.get_system_by_id(order['pay_system_id'])

    crypto_cur = pay_systems.get_currency_by_id(user['base_currency_id'])

    fiat_cur = pay_systems.get_currency_by_id(user['base_fiat_currency_id'])

    user_currency_id = users.get_user_by_tgid(update.effective_user.id)['base_currency_id']
    user_currency = pay_systems.get_currency_by_id(user_currency_id)

    if user_data[info['message'].message_id]['trade'] == 'buy':
        message = _(texts.buy_order_)
    else:
        message = _(texts.sell_order_)

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

    keyboard = [[InlineKeyboardButton(_(texts.cancel_), callback_data='trade system {}'.format(order['pay_system_id'])),
                InlineKeyboardButton(_(texts.start_deal_), callback_data='trade start_deal {}'.format(order_id))]]

    info['message'].edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
