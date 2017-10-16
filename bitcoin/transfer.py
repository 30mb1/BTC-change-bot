from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import texts
from database import *
from utils.decorators import info

MENU, WITHDRAW, CHOOSE_TYPE, PAY_SYSTEM, RATE, LIMMITS = range(6)

@info
def check_address(_, info, bot, update, user_data):
    print ('checking address')
    address = info['message'].text

    #check address for mistakes

    #if wrng
    #update.message.reply_text(texts.incorrect_input_)
    #return WITHDRAW

    #if ok, return to WITHDRAW and check for amount
    info['message'].reply_text(texts.chk_addr_ok_)
    user_data['checking_address'] = False

    return WITHDRAW

@info
def check_balance(_, info, bot, update, user_data):
    #check for valid input
    try:
        sum_to_withdraw = float(info['message'].text)
        if sum_to_withdraw <= 0:
            raise Exception
    except:
        info['message'].reply_text(texts.incorrect_input_)
        return False

    #check if user have enough funds
    if payments.withdraw_money(info['tg_id'], sum_to_withdraw):
        return True

    info['message'].reply_text(texts.low_funds_)
    return False

def get_address(user_id):
    return 'btc address for user should be here'

@info
def withdraw(_, info, bot, update, user_data):
    menu_keyboard = [['💰 Кошелек', '📊 Купить/продать'], ['ℹ О сервисе', '🔩 Настройки']]

    #print (user_data)

    #check address for validity
    if user_data.get('checking_address', True):
        return check_address(bot, update, user_data=user_data)

    #check sum
    if check_balance(bot, update, user_data=user_data):
        message = texts.chk_sum_ok_
        info['message'].reply_text(message, reply_markup=ReplyKeyboardMarkup(menu_keyboard))

        user_data.pop('checking_address')
        #send money to withdraw address of user
    else:
        return WITHDRAW

    return MENU
