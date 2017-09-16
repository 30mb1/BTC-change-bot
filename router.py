from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler, Filters
from wallet import wallet as w
from trade import trade as t


def query_route(bot, update, user_data):
    query = update.callback_query
    data = query.data.split()

    if 'wallet' in data:
        return w.query_route(bot, update, user_data)

    if 'trade' in data:
        return t.query_route(bot, update, user_data)


    
