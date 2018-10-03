from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import texts
from instruments import settings
from utils.decorators import info

MENU, WITHDRAW, CHOOSE_TYPE, PAY_SYSTEM, RATE, LIMMITS = range(6)

@info
def show_instruments(_, info, bot, update, user_data):
    keyboard = [[InlineKeyboardButton(texts.choose_fiat_, callback_data='settings choose_fiat from_settings'),
                InlineKeyboardButton(texts.choose_crypto_, callback_data='settings choose_crypto from_settings')]]

    message = _(texts.settings_msg_)

    if info['callback']:
        info['message'].edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    info['message'].reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@info
def query_route(_, info, bot, update, user_data):
    if info['data'][1] == 'set_fiat' or info['data'][1] == 'set_crypto':
        settings.set_currency(bot, update, user_data=user_data)

    if info['data'][1] == 'choose_crypto' or info['data'][1] == 'choose_fiat':
        settings.choose_currency(bot, update, user_data=user_data)

    elif info['data'][1] == 'cancel':
        show_instruments(bot, update, user_data=user_data)

@info
def about_us(_, info, bot, update, user_data):
    update.message.reply_text('BEST BOT FOR TRADING THIS WORLD HAS EVER SEEN')
