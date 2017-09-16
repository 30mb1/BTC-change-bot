from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import (Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler,
                        Filters, CallbackQueryHandler)
import texts
from database import payments

MENU, WITHDRAW = range(2)
menu_keyboard = [['💰 Кошелек', '📊 Купить/продать BTC'], ['ℹ О сервисе', '🔩 Настройки']]

def check_address(bot, update, user_data):
    print ('checking address')
    address = update.message.text

    #check address for mistakes

    #if wrng
    #update.message.reply_text(texts.incorrect_input_)
    #return WITHDRAW

    #if ok, return to WITHDRAW and check for amount
    update.message.reply_text(texts.chk_addr_ok_)
    user_data['cheking_address'] = False

    return WITHDRAW

def check_balance(bot, update, user_data):
    #check for valid input
    try:
        sum_to_withdraw = float(update.message.text)
        if sum_to_withdraw <= 0:
            raise Exception
    except:
        update.message.reply_text(texts.incorrect_input_)
        return False

    #check if user have enough funds
    if payments.withdraw_money(update.message.from_user.id, sum_to_withdraw):
        return True

    update.message.reply_text(texts.low_funds_)
    return False


def get_address(user_id):
    return 'btc address for user should be here'

def withdraw(bot, update, user_data):

    #print (user_data)

    #check address for validity
    if user_data.get('cheking_address', True):
        return check_address(bot, update, user_data)

    #check sum
    if check_balance(bot, update, user_data):
        message = texts.chk_sum_ok_
        update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(menu_keyboard))

        user_data.pop('cheking_address')
        #send money to withdraw address of user
    else:
        return WITHDRAW

    return MENU
