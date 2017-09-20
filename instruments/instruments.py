from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
import texts
from instruments import settings

MENU, WITHDRAW = range(2)

def show_instruments(bot, update, user_data):

    keyboard = [[InlineKeyboardButton(texts.choose_fiat_, callback_data='settings choose_fiat from_settings'),
                InlineKeyboardButton(texts.choose_crypto_, callback_data='settings choose_crypto from_settings')]]

    message = texts.settings_msg_

    if update.callback_query:
        update.callback_query.message.edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

def query_route(bot, update, user_data):
    query = update.callback_query
    data = query.data.split()[1]

    if data == 'set_fiat' or data == 'set_crypto':
        settings.set_currency(bot, update, user_data)
    if data == 'choose_crypto' or data == 'choose_fiat':
        settings.choose_currency(bot, update, user_data)
    elif data == 'cancel':
        show_instruments(bot, update, user_data)

def about_us(bot, update):
    update.message.reply_text('This section is in progress')
