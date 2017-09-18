from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import bitcoin
import texts
from trade import trade
from database import pay_systems
from decimal import *

PAGE_SIZE = 3

MENU, WITHDRAW = range(2)

def show_pay_systems(bot, update, user_data):
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data.split()[1]
    page = user_data[msg_id]['page']
    from_ = page
    to_ = page + PAGE_SIZE

    #we know base_fiat_currency for every user. Getting list of available methods for selected currency
    systems = pay_systems.get_pay_systems_list(update.callback_query.from_user.id)

    #store only systems where advs are
    #if user_data[msg_id]['trade'] == 'buy':
    #    systems = [item for item in systems if item['sell_count'] != 0]
    #else:
    #    systems = [item for item in systems if item['buy_count'] != 0]

    #if there are no advs at all, show appropriate mesage
    #if len(systems) == 0:
    #    bot.send_message(text=texts.no_advs_.format('RUB'), chat_id=update.callback_query.from_user.id)
    #    return

    #checking which button was pressed bu the user
    if data == 'next_systems':

        #increase page counter for this message
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] + 1

        #show only PAGE_SIZE pay systems on one page
        #check if we have not full pages
        if len(systems) % PAGE_SIZE != 0:
            page = page % int(len(systems) / PAGE_SIZE + 1)
        else:
            page = page % int(len(systems) / PAGE_SIZE)

        from_ = page * PAGE_SIZE
        to_ = from_ + PAGE_SIZE

    elif data == 'back_systems':
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] - 1

        if len(systems) % PAGE_SIZE != 0:
            page = page % int(len(systems) / PAGE_SIZE + 1)
        else:
            page = page % int(len(systems) / PAGE_SIZE)

        from_ = page * PAGE_SIZE
        to_ = from_ + PAGE_SIZE

    #choosing appropriate message
    if user_data[msg_id]['trade'] == 'buy':
        message = texts.buy_text_.format(12345)
    else:
        message = texts.sell_text_.format(12345)

    keyboard = [[InlineKeyboardButton(item['name'], callback_data='trade system {}'.format(item['id']))] for item in systems[from_:to_]]

    #manually adding next/cancel/back row of buttons
    keyboard.append(
        [InlineKeyboardButton(texts.back_, callback_data='trade back_systems'),
        InlineKeyboardButton(texts.cancel_, callback_data='trade cancel'), InlineKeyboardButton(texts.next_, callback_data='trade next_systems')]
    )

    #using 'trade' in callback data for simplificaion of routing callback queries

    update.callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

def show_orders(bot, update, user_data):
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data.split()

    trend = data[1]
    pay_system_id = data[2]


    if user_data[msg_id]['trade'] == 'buy':
        buy = 1
    else:
        buy = 0

    orders = pay_systems.get_orders_for_system(update.callback_query.from_user.id, buy, pay_system_id)

    page = user_data[msg_id]['page']
    from_ = page
    to_ = page + PAGE_SIZE


    #checking which button was pressed bu the user
    if trend == 'next_orders':

        #increase page counter for this message
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] + 1

        #show only PAGE_SIZE pay systems on one page
        #check if we have not full pages
        if len(orders) % PAGE_SIZE != 0:
            page = page % int(len(orders) / PAGE_SIZE + 1)
        else:
            page = page % int(len(orders) / PAGE_SIZE)

        from_ = page * PAGE_SIZE
        to_ = from_ + PAGE_SIZE

    elif trend == 'back_orders':
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] - 1

        if len(orders) % PAGE_SIZE != 0:
            page = page % int(len(orders) / PAGE_SIZE + 1)
        else:
            page = page % int(len(orders) / PAGE_SIZE)

        from_ = page * PAGE_SIZE
        to_ = from_ + PAGE_SIZE

    system_name = pay_systems.get_system_name_by_id(pay_system_id)

    if user_data[msg_id]['trade'] == 'buy':
        message = texts.buy_list_.format(len(orders), system_name)
    else:
        message = texts.sell_list_.format(len(orders), system_name)

    keyboard = []

    for i in orders[from_:to_]:

        button_sign = "{} ({} - {}) {}".format(i['rate'].quantize(Decimal('.01')), i['min'].quantize(Decimal('.01')), i['max'].quantize(Decimal('.01')), i['user_id'])
        keyboard.append([InlineKeyboardButton(button_sign, callback_data='trade order {}'.format(pay_system_id))])

    #manually adding next/cancel/back row of buttons
    keyboard.append(
        [InlineKeyboardButton(texts.back_, callback_data='trade back_orders {}'.format(pay_system_id)),
        InlineKeyboardButton(texts.cancel_, callback_data='trade cancel'), InlineKeyboardButton(texts.next_, callback_data='trade next_orders {}'.format(pay_system_id))]
    )

    #using 'trade' in callback data for simplificaion of routing callback queries

    update.callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )