import logging
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode

from telegram.ext import (Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler,
                          Filters, CallbackQueryHandler)

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

from telegram.ext.dispatcher import run_async
from wallet import wallet as w
from trade import trade as t
from instruments import instruments as i
import admin as a
from bitcoin import transfer
import texts
from database import users
import json
from utils.router import query_route


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Main')

MENU, WITHDRAW, CHOOSE_TYPE, PAY_SYSTEM, RATE, LIMMITS, DESCRIPTION = range(7)

menu_keyboard = [['💰 Кошелек', '📊 Купить/продать'], ['ℹ О сервисе', '🔩 Настройки']]


def error_callback(bot, update, error):
    try:
        raise error
    except Exception as e:
        print(e)


def start(bot, update, user_data):
    user_data['lang'] = 'ru'
    #gettext.install('messages', './locale')
    message = texts.start_

    users.register_user(json.loads(update.message.from_user.to_json()))

    update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(menu_keyboard))

    return MENU


def cancel(bot, update, user_data):
    # delete all temporary data except user language
    lang = user_data['lang']
    user_data.clear()
    user_data['lang'] = lang
    update.message.reply_text(texts.canceled_, reply_markup=ReplyKeyboardMarkup(menu_keyboard))
    return MENU


def main():
    updater = Updater(token='383099020:AAG_L-5NahITmUTdJoYTSWMBX7n5561Pa8I', workers=32)
    dispatcher = updater.dispatcher

    dispatcher.add_error_handler(error_callback)

    main_menu = ConversationHandler(

        entry_points=[CommandHandler('start', start, pass_user_data=True)],

        states={

            # regular expression for all languages should be here.
            MENU: [
                RegexHandler('^(💰 Кошелек)$', w.show_wallet, pass_user_data=True),
                RegexHandler('^(📊 Купить/продать)$', t.show_trade, pass_user_data=True),
                RegexHandler('^(🔩 Настройки)$', i.show_instruments, pass_user_data=True),
                RegexHandler('^(ℹ О сервисе)$', i.about_us, pass_user_data=True)
            ],

            WITHDRAW: [
                RegexHandler('^(Отмена)$', cancel, pass_user_data=True),
                MessageHandler(Filters.text, transfer.withdraw, pass_user_data=True)
            ],

            # states for creating new order
            CHOOSE_TYPE: [
                RegexHandler('^(Отмена)$', cancel, pass_user_data=True),
                MessageHandler(Filters.text, a.create.get_type, pass_user_data=True)
            ],

            PAY_SYSTEM: [
                RegexHandler('^(Назад)$', a.create.create_order, pass_user_data=True),
                MessageHandler(Filters.text, a.create.get_pay_system, pass_user_data=True)
            ],

            RATE: [
                RegexHandler('^(Назад)$', a.create.get_type, pass_user_data=True),
                MessageHandler(Filters.text, a.create.get_rate, pass_user_data=True)
            ],

            DESCRIPTION: [
                RegexHandler('^(Назад)$', a.create.get_pay_system, pass_user_data=True),
                MessageHandler(Filters.text, a.create.get_description, pass_user_data=True)
            ],

            LIMMITS: [
                RegexHandler('^(Назад)$', a.create.get_pay_system, pass_user_data=True),
                MessageHandler(Filters.text, transfer.withdraw, pass_user_data=True)
            ]
        },

        fallbacks=[CallbackQueryHandler(query_route, pass_user_data=True)],
        allow_reentry=True
    )

    dispatcher.add_handler(main_menu)
    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()
 
