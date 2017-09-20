import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import (Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler,
                        Filters, CallbackQueryHandler)
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext.dispatcher import run_async
from wallet import wallet as w
from trade import trade as t
from instruments import instruments as i
import router
from bitcoin import transfer
import gettext
import texts
from database import users
from ast import literal_eval


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Main')

MENU, WITHDRAW = range(2)

menu_keyboard = [['💰 Кошелек', '📊 Купить/продать'], ['ℹ О сервисе', '🔩 Настройки']]


def error_callback(bot, update, error):
    try:
        raise error
    except Exception as e:
        print (e)


def start(bot, update, user_data):
    #user_data['ru'] = gettext.translation('messages', localedir='./locale', languages=['ru'])
    #user_data['en'] = gettext.translation('messages', localedir='./locale', languages=['en'])
    #user_data['lang'] = gettext.gettext
    #gettext.install('messages', './locale')
    message = texts.start_

    #print (literal_eval(update.message.from_user.to_json()))
    users.register_user(literal_eval(update.message.from_user.to_json()))

    update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(menu_keyboard))

    return MENU


def cancel(bot, update, user_data):
    user_data.clear()
    update.message.reply_text(texts.canceled_, reply_markup=ReplyKeyboardMarkup(menu_keyboard))
    return MENU


def main():
    updater = Updater(token='383099020:AAG_L-5NahITmUTdJoYTSWMBX7n5561Pa8I',workers=32)
    dispatcher = updater.dispatcher

    dispatcher.add_error_handler(error_callback)

    main_menu = ConversationHandler(

        entry_points=[CommandHandler('start', start, pass_user_data=True)],

        states={

            #regular expression for all languages should be here.
            MENU : [
                RegexHandler('^(💰 Кошелек)$', w.show_wallet, pass_user_data=True),
                RegexHandler('^(📊 Купить/продать)$', t.show_trade),
                RegexHandler('^(🔩 Настройки)$', i.show_instruments, pass_user_data=True),
                RegexHandler('^(ℹ О сервисе)$', i.about_us)
            ],

            WITHDRAW : [
                RegexHandler('Отмена', cancel, pass_user_data=True),
                MessageHandler(Filters.text, transfer.withdraw, pass_user_data=True)
            ]
        },

        fallbacks=[CallbackQueryHandler(router.query_route, pass_user_data=True)],
        allow_reentry=True
    )


    dispatcher.add_handler(main_menu)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
