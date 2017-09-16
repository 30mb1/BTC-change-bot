from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler, Filters
import bitcoin
import texts
from trade import trade
from database import pay_systems

MENU, WITHDRAW = range(2)

def show_pay_systems(bot, update, user_data):
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data.split()[1]
    page = user_data[msg_id]['page']
    from_ = page
    to_ = page + 3

    #tmp solution, currency later will be stored in user_data for everyone
    systems = pay_systems.get_list('RUB')

    #store only systems where advs are
    if user_data[msg_id]['trade'] == 'buy':
        systems = [item for item in systems if item['sell_count'] != 0]
    else:
        systems = [item for item in systems if item['buy_count'] != 0]

    #if there are no advs at all, show appropriate mesage
    if len(systems) == 0:
        bot.send_message(text=texts.no_advs_.format('RUB'), chat_id=update.callback_query.from_user.id)
        return

    #checking which button was pressed bu the user
    if data == 'next_systems':

        #increase page counter for this message
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] + 1

        #show only 3 pay systems on one page
        #check if we have not full pages
        if len(systems) % 3 != 0:
            page = page % int(len(systems) / 3 + 1)
        else:
            page = page % int(len(systems) / 3)

        from_ = page * 3
        to_ = from_ + 3

    elif data == 'back_systems':
        page = user_data[msg_id]['page'] = user_data[msg_id]['page'] - 1

        if len(systems) % 3 != 0:
            page = page % int(len(systems) / 3 + 1)
        else:
            page = page % int(len(systems) / 3)

        from_ = page * 3
        to_ = from_ + 3

    #choosing appropriate message
    if user_data[msg_id]['trade'] == 'buy':
        message = texts.buy_text_.format(12345)
    else:
        message = texts.sell_text_.format(12345)

    keyboard = []

    for item in systems[from_:to_]:

        #check if user want to buy or to sell BTC and choose appropriate information for showing
        if user_data[msg_id]['trade'] == 'buy':
            button_sign = ' '.join([item['name'], str(item['best_sell']), str(item['sell_count'])])
        else:
            button_sign = ' '.join([item['name'], str(item['best_buy']), str(item['buy_count'])])

        keyboard.append([InlineKeyboardButton(button_sign, callback_data=item['name'])])

    #manually adding next/cancel/back row of buttons
    keyboard.append(
        [InlineKeyboardButton(texts.back_, callback_data='trade back_systems'),
        InlineKeyboardButton(texts.cancel_, callback_data='trade cancel'), InlineKeyboardButton(texts.next_, callback_data='trade next_system')]
    )

    #using 'trade' in callback data for simplificaion of routing callback queries

    update.callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

def show_ads(bot, udpate, user_data):
    return
