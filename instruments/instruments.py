from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler, Filters
import bitcoin

MENU, ADDRESS_INPUT = range(2)


def show_settings(bot, update, user_data):
    update.message.reply_text('This section is in progress')
    return MENU

def about_us(bot, update):
    update.message.reply_text('This section is in progress')
    return MENU
