from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import texts
from database import *
from decimal import *
from utils.decorators import info
import re

MENU, WITHDRAW, CHOOSE_TYPE, PAY_SYSTEM, RATE, LIMMITS, DESCRIPTION = range(7)
menu_keyboard = [['💰 Кошелек', '📊 Купить/продать'], ['ℹ О сервисе', '🔩 Настройки']]


@info
def create_order(_, info, bot, update, user_data):
    currency_id = users.get_user_by_tgid(info['tg_id'])['base_currency_id']
    currency = pay_systems.get_currency_by_id(currency_id)

    keyboard = [[_(texts.buy_).format(currency['name'])], [_(texts.sell_).format(currency['name'])], [_(texts.cancel_)]]

    info['message'].reply_text(text=_(texts.adv_create_1_), reply_markup=ReplyKeyboardMarkup(keyboard))

    #create temporary storage for new order data
    user_data['create_order'] = {}
    return CHOOSE_TYPE

@info
def get_type(_, info, bot, update, user_data):
    message_text = info['message'].text

    user = users.get_user_by_tgid(info['tg_id'])
    currency = pay_systems.get_currency_by_id(user['base_currency_id'])

    #in order not to use regex, check user input manually
    #create input choices
    buy = _(texts.buy_).format(currency['name'])
    sell = _(texts.sell_).format(currency['name'])

    #compare user input and prepared choices and store result in user_data until the process is finished
    if message_text == buy:
        user_data['create_order']['base_currency_id'] = user['base_fiat_currency_id']
        user_data['create_order']['ref_currency_id'] = user['base_currency_id']
    elif message_text == sell:
        user_data['create_order']['base_currency_id'] = user['base_currency_id']
        user_data['create_order']['ref_currency_id'] = user['base_fiat_currency_id']
    elif message_text == _(texts.back_):
        #we already have chosen order type and just want to rechoose pay system
        pass
    else:
        #incorrect input
        info['message'].reply_text(_(texts.incorrect_input_))
        return CHOOSE_TYPE

    available_pay_systems = pay_systems.get_available_pay_systems(info['tg_id'], user_data['create_order'])
    keyboard = [[pay_system] for pay_system in available_pay_systems]
    keyboard.append([_(texts.back_)])

    info['message'].reply_text(_(texts.adv_create_2_), reply_markup=ReplyKeyboardMarkup(keyboard))

    #store list of available pay systems for checking input on next step.
    user_data['create_order']['available_systems'] = available_pay_systems
    return PAY_SYSTEM

@info
def get_pay_system(_, info, bot, update, user_data):
    message_text = info['message'].text

    if message_text in user_data['create_order']['available_systems']:
        user_data['create_order']['pay_system'] = message_text
    elif message_text == _(texts.back_):
        #we already have chosen pay_system and just want to rechoose rate
        pass
    else:
        info['message'].reply_text(_(texts.incorrect_input_))
        return PAY_SYSTEM

    info['message'].reply_text(_(texts.adv_create_3_), reply_markup=ReplyKeyboardMarkup([[_(texts.back_)]]))
    return RATE

@info
def get_rate(_, info, bot, update, user_data):
    message_text = info['message'].text

    if message_text == _(texts.back_):
        info['message'].reply_text(_(texts.adv_create_4_), reply_markup=ReplyKeyboardMarkup([[_(texts.back_)]]))
        return DESCRIPTION
    else:
        try:
            price = int(message_text)
            user_data['create_order']['rate'] = price
            print (price)
            info['message'].reply_text(_(texts.adv_create_4_), reply_markup=ReplyKeyboardMarkup([[_(texts.back_)]]))
            return DESCRIPTION
        except Exception as e:
            price = re.match('(?:\d+)', message_text)
            if price:
                price = price.group(0)
                price = int(240000 * (int(price) / 100))
                user_data['create_order']['rate'] = price
                print (price)
                info['message'].reply_text(_(texts.adv_create_4_), reply_markup=ReplyKeyboardMarkup([[_(texts.back_)]]))
                return DESCRIPTION
            info['message'].reply_text(_(texts.incorrect_input_))
            return RATE

@info
def get_description(_, info, bot, update, user_data):
    message_text = info['message'].text
    user_ = users.get_user_by_tgid(info['tg_id'])

    user_data['create_order']['message'] = message_text
    order.create_order(user_['id'], user_data['create_order'])

    update.message.reply_text(texts.adv_created, reply_markup=ReplyKeyboardMarkup(menu_keyboard))

    return MENU
