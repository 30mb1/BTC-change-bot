
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import (Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler,
                        Filters, CallbackQueryHandler)

MENU = 0
menu_keyboard = [['💰 Wallet', '📊 Exchange'], ['ℹ About us', '🔩 Settings']]


def get_address(user_id):
    return 'btc address for user should be here'

def withdraw(bot, update):
    address = update.message.text

    #check address for mistakes

    #check if user have enough funds (some funds may be blocked because of trade)

    message = 'Ok, payment sent to address {}'.format(address)

    update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(menu_keyboard))

    return MENU
