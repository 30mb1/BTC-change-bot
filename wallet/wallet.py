from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler, Filters
from bitcoin import bitcoin
import texts
from database import users

MENU, WITHDRAW = range(2)


def show_wallet(bot, update, user_data):
    keyboard = [
        [InlineKeyboardButton(texts.deposit_, callback_data='wallet deposit'),
        InlineKeyboardButton(texts.withdraw_, callback_data='wallet withdraw')]
    ]
    #_ = user_data['lang']
    message = texts.wallet_msg_.format(users.get_user_balance(update.message.from_user.id), 254000)

    update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

def query_route(bot, update, user_data):
    query = update.callback_query
    data = query.data.split()[1]

    if data == 'withdraw':
        message = texts.withdraw_msg_
        bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            reply_markup=ReplyKeyboardMarkup([[texts.cancel_]]),
            parse_mode=ParseMode.MARKDOWN
        )
        return WITHDRAW
    else:
        message = texts.deposit_msg_

        bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text="*{}*".format(bitcoin.get_address(query.message.from_user.id)),
            parse_mode=ParseMode.MARKDOWN
        )
