from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler, Filters
import bitcoin
import texts

MENU, ADDRESS_INPUT = range(2)


def show_wallet(bot, update, user_data):
    keyboard = [
        [InlineKeyboardButton("Deposit", callback_data='wallet deposit'),
        InlineKeyboardButton("Withdraw", callback_data='wallet withdraw')]
    ]
    #_ = user_data['lang']
    message = "*BTC Wallet*\n*Balance*: 0  BTC\n*Equivalent*: 0 RUB"

    update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

    return MENU


def query_route(bot, update):
    query = update.callback_query
    data = query.data.split()[1]

    if data == 'withdraw':
        message = '📤 *Withdraw Bitcoin*\n\nPlease enter the address of the external BTC wallet.'
        bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            reply_markup=ReplyKeyboardMarkup([['Cancel']]),
            parse_mode=ParseMode.MARKDOWN
        )
        return ADDRESS_INPUT
    else:
        message = "📥 *Deposit Bitcoin*\n\nUse the address below to deposit BTC from an external wallet.\n*{}*".format(bitcoin.get_address(query.message.from_user.id))

        bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )

        return MENU
