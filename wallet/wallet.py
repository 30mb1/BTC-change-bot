from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from bitcoin import transfer
import texts
from database import *
from utils.decorators import info

MENU, WITHDRAW, CHOOSE_TYPE, PAY_SYSTEM, RATE, LIMMITS = range(6)

@info
def show_wallet(info, bot, update, user_data):
    keyboard = [
        [InlineKeyboardButton(texts.deposit_, callback_data='wallet deposit'),
        InlineKeyboardButton(texts.withdraw_, callback_data='wallet withdraw')]
    ]
    #_ = user_data['lang']
    message = texts.wallet_msg_.format(users.get_user_account(update.effective_user.id)['balance'], 254000)

    info['message'].reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@info
def query_route(info, bot, update, user_data):
    if info['data'][1] == 'withdraw':
        message = texts.withdraw_msg_
        info['message'].reply_text(
            text=message,
            reply_markup=ReplyKeyboardMarkup([[texts.cancel_]])
        )
        return WITHDRAW
    else:
        message = texts.deposit_msg_
        info['message'].reply_text(text=message)
        info['message'].reply_text(text="*{}*".format(transfer.get_address(info['tg_id'])))
