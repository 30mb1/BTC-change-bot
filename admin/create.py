from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import texts
from database import *
from decimal import *
from utils.decorators import info

MENU, WITHDRAW, CHOOSE_TYPE, PAY_SYSTEM, RATE, LIMMITS = range(6)

@info
def create_order(info, bot, update, user_data):
    currency_id = users.get_user_by_tgid(info['tg_id'])['base_currency_id']
    currency = pay_systems.get_currency_by_id(currency_id)

    keyboard = [[texts.buy_.format(currency['name'])], [texts.sell_.format(currency['name'])], [texts.cancel_]]

    info['message'].reply_text(text=texts.adv_create_1_, reply_markup=ReplyKeyboardMarkup(keyboard))

    #create temporary storage for new order data
    user_data['create_order'] = {}
    return CHOOSE_TYPE

@info
def get_type(info, bot, update, user_data):
    message_text = info['message'].text

    user = users.get_user_by_tgid(info['tg_id'])
    currency = pay_systems.get_currency_by_id(user['base_currency_id'])

    #in order not to use regex, check user input manually
    #create input choices
    buy = texts.buy_.format(currency['name'])
    sell = texts.sell_.format(currency['name'])

    #compare user input and prepared choices and store result in user_data until the process is finished
    if message_text == buy:
        user_data['create_order']['base_currency_id'] = user['base_fiat_currency_id']
        user_data['create_order']['ref_currency_id'] = user['base_currency_id']
    elif message_text == sell:
        user_data['create_order']['base_currency_id'] = user['base_currency_id']
        user_data['create_order']['ref_currency_id'] = user['base_fiat_currency_id']
    elif message_text == texts.back_:
        #we already have chosen order type and just want to rechoose pay system
        pass
    else:
        #incorrect input
        info['message'].reply_text(texts.incorrect_input_)
        return CHOOSE_TYPE

    available_pay_systems = pay_systems.get_available_pay_systems(info['tg_id'], user_data['create_order'])
    keyboard = [[pay_system] for pay_system in available_pay_systems]
    keyboard.append([texts.back_])

    info['message'].reply_text(texts.adv_create_2_, reply_markup=ReplyKeyboardMarkup(keyboard))

    #store list of available pay systems for checking input on next step.
    user_data['create_order']['available_systems'] = available_pay_systems
    return PAY_SYSTEM

@info
def get_pay_system(info, bot, update, user_data):
    message_text = info['message'].text

    if message_text in user_data['create_order']['available_systems']:
        user_data['create_order']['pay_system'] = message_text
    elif message_text == texts.back_:
        #we already have chosen pay_system and just want to rechoose rate
        pass
    else:
        info['message'].reply_text(texts.incorrect_input_)
        return RATE

    info['message'].reply_text(texts.adv_create_3_, reply_markup=ReplyKeyboardMarkup([[texts.back_]]))
    return RATE

@info
def get_rate(info, bot, update, user_data):
    return
