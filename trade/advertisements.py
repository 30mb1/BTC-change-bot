from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from database import users

def show_advertisements(bot, update, user_data):
    user_id = update.callback_query.from_user.id
    message = texts.advs_msg_.format(99999)

    keyboard = []

    for deal in users.get_advs_by_user(user_id):
        trade = texts.buy_ if deal['trade'] == 'but' else texts.sell_
        visible  = '' if deal['visible'] == True else '[OFF]'
        name = deal['name']
        rate = str(deal['rate'])
        button_sign = ' '.join(trade, visible, name, rate)
        keyboard.append([InlineKeyboardButton(button_sign, callback_data='trade ' + deal['id'])])

    keyboard.append(
        [InlineKeyboardButton(texts.add_, callback_data='trade create'),
        InlineKeyboardButton(texts.back_, callback_data='trade cancel')]
    )

    update.callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

def create_advertisement(bot, update, user_data):
    keyboard = [[texts.adv_create_2_], [texts.adv_create_3_], [texts.cancel_]]
    bot.send_message(chat_id=update.callback_query.from_user.id, text=texts.adv_create_1_, reply_markup=ReplyKeyboardMarkup(keyboard))

    return
