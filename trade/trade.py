from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler, Filters
import bitcoin

MENU, ADDRESS_INPUT = range(2)


def show_trade(bot, update):
    message = "📊 *Buy/Sell BTC*\n\nHere you can deal with people.\n\nMarket rate: 999999 RUB"

    keyboard = [
        [InlineKeyboardButton("Buy 📉", callback_data='trade buy'),
        InlineKeyboardButton("Sell 📈", callback_data='trade sell')]
    ]

    update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

    return MENU
