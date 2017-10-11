from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler, Filters
from wallet import wallet as w
from trade import trade as t
from admin import admin as a
from instruments import instruments as i

def info(func):
    def wrapper(*args, **kwargs):
        extracted_info = {}
        update = args[1]
        extracted_info['tg_id'] = update.effective_user.id
        extracted_info['chat_id'] = update.effective_chat.id
        extracted_info['message'] = update.effective_message
        if update.callback_query:
            extracted_info['callback'] = True
            extracted_info['data'] = update.callback_query.data.split()

        res = func(extracted_info, *args, **kwargs)

        if update.callback_query:
            update.callback_query.answer()

        return res
    return wrapper

@info
def query_route(bot, update, user_data):
    if 'wallet' in info['data']:
        return w.query_route(bot, update, user_data)

    if 'trade' in info['data']:
        return t.query_route(bot, update, user_data)

    if 'admin' in info['data']:
        return a.query_route(bot, update, user_data)

    if 'settings' in info['data']:
        return i.query_route(bot, update, user_data)
