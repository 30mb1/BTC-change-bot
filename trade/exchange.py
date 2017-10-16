from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import texts
from database import *
from decimal import *
from utils.decorators import info

PAGE_SIZE = 3

MENU, WITHDRAW, CHOOSE_TYPE, PAY_SYSTEM, RATE, LIMMITS = range(6)

@info
def show_pay_systems(info, bot, update, user_data):
    msg_id = info['message'].message_id
    page = user_data[msg_id]['page']

    #cryptocurrency selected ny user
    user_currency_id = users.get_user_by_tgid(info['tg_id'])['base_currency_id']
    user_currency = pay_systems.get_currency_by_id(user_currency_id)

    #we know base_fiat_currency for every user. Getting list of available methods for selected currency
    systems = pay_systems.get_pay_systems_list(info['tg_id'])

    paginated_systems = [systems[i:i + PAGE_SIZE] for i in range(0, len(systems), PAGE_SIZE)]
    #store only systems where advs are

    #checking which button was pressed bu the user
    if info['data'][1] == 'next_systems':

        #increase page counter for this message
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] + 1
        page = page % len(paginated_systems)

    elif info['data'][1] == 'back_systems':
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] - 1
        page = page % len(paginated_systems)

    #choosing appropriate message
    message = texts.buy_text_ if user_data[msg_id]['trade'] == 'buy' else texts.sell_text_
    message = message.format(user_currency['name'], 240000)

    keyboard = []
    if len(paginated_systems):
        keyboard = [[InlineKeyboardButton(item['name'], callback_data='trade system {}'.format(item['id']))] for item in paginated_systems[page]]

    #manually adding next/cancel/back row of buttons
    keyboard.append(
        [InlineKeyboardButton(texts.back_, callback_data='trade back_systems'),
        InlineKeyboardButton(texts.cancel_, callback_data='trade cancel'),
        InlineKeyboardButton(texts.next_, callback_data='trade next_systems')]
    )

    #using 'trade' in callback data for simplificaion of routing callback queries

    info['message'].edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@info
def show_system_orders(info, bot, update, user_data):
    msg_id = info['message'].message_id

    trend = info['data'][1]
    pay_system_id = info['data'][2]

    buy = 0 if user_data[msg_id]['trade'] == 'buy' else 1

    user_currency_id = users.get_user_by_tgid(info['tg_id'])['base_currency_id']
    user_currency = pay_systems.get_currency_by_id(user_currency_id)

    orders = pay_systems.get_orders_for_system(info['tg_id'], buy, pay_system_id)

    paginated_orders = [orders[i:i + PAGE_SIZE] for i in range(0, len(orders), PAGE_SIZE)]

    page = user_data[msg_id]['page']

    #checking which button was pressed bu the user
    if trend == 'next_orders':

        #increase page counter for this message
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] + 1
        page = page % len(paginated_orders)


    elif trend == 'back_orders':
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] - 1
        page = page % len(paginated_orders)

    system_name = pay_systems.get_system_by_id(pay_system_id)['name']

    message = texts.buy_list_ if user_data[msg_id]['trade'] == 'buy' else texts.sell_list_
    message = message.format(user_currency['name'], len(orders), system_name)

    #get symbol of fiat currency for selected pay_system
    currency_id = pay_systems.get_system_by_id(pay_system_id)['currency_id']
    currency = pay_systems.get_currency_by_id(currency_id)
    symbol = currency['symbol']

    keyboard = []

    if len(paginated_orders):
        for i in paginated_orders[page]:
            user = users.get_user_by_usid(i['user_id'])

            button_sign = "{} {} ({} - {} {}) {}".format(
                                                    i['rate'].quantize(Decimal('.01')),
                                                    symbol,
                                                    i['min'].quantize(Decimal('.01')),
                                                    i['max'].quantize(Decimal('.01')),
                                                    symbol,
                                                    user['username']
                                                )

            keyboard.append([InlineKeyboardButton(button_sign, callback_data='trade show_order {}'.format(i['id']))])

    #manually adding next/cancel/back row of buttons
    #using 'trade' in callback data for simplificaion of routing callback queries
    keyboard.append(
        [InlineKeyboardButton(texts.back_, callback_data='trade back_orders {}'.format(pay_system_id)),
        InlineKeyboardButton(texts.cancel_, callback_data='trade {}'.format(user_data[msg_id]['trade'])),
        InlineKeyboardButton(texts.next_, callback_data='trade next_orders {}'.format(pay_system_id))]
    )

    info['message'].edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
