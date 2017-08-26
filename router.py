from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler, Filters
from wallet import wallet as w


def query_route(bot, update):
    query = update.callback_query
    data = query.data.split()

    if 'wallet' in data:
        return w.query_route(bot, update)
