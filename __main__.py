# -*- coding: utf-8 -*-
import logging
import logging.handlers
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton,
                    InlineKeyboardMarkup, ParseMode)
from telegram.ext import (Updater, ConversationHandler, RegexHandler, CommandHandler, MessageHandler,
                        Filters, CallbackQueryHandler)
from wallet import wallet as w
from trade import trade as t
from instruments import instruments as i
import router
import bitcoin
import gettext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

MENU, ADDRESS_INPUT = range(2)

menu_keyboard = [['💰 Wallet', '📊 Exchange'], ['ℹ About us', '🔩 Settings']]

def start(bot, update, user_data):
    #user_data['ru'] = gettext.translation('messages', localedir='./locale', languages=['ru'])
    #user_data['en'] = gettext.translation('messages', localedir='./locale', languages=['en'])
    #user_data['lang'] = gettext.gettext
    #gettext.install('messages', './locale')

    message = "Hello, welcome to BTC-change bot. It's a p2p change bot with Escrow service, so that we guarantee safety of your funds"

    update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup(menu_keyboard))

    return MENU

def cancel(bot, update):
    update.message.reply_text('Cancelled')
    return MENU


def main():
    updater = Updater(token='383099020:AAG_L-5NahITmUTdJoYTSWMBX7n5561Pa8I')
    dispatcher = updater.dispatcher


    main_menu = ConversationHandler(

        entry_points=[CommandHandler('start', start, pass_user_data=True)],

        states={

            MENU : [
                RegexHandler('^(💰 Wallet)$', w.show_wallet, pass_user_data=True),
                RegexHandler('^(📊 Exchange)$', t.show_trade),
                RegexHandler('^(🔩 Settings)$', i.show_settings, pass_user_data=True),
                RegexHandler('^(ℹ About us)$', i.about_us)
            ],

            ADDRESS_INPUT : [
                RegexHandler('Cancel', cancel),
                MessageHandler(Filters.text, bitcoin.withdraw)
            ]
        },

        fallbacks=[CallbackQueryHandler(router.query_route)]
    )


    dispatcher.add_handler(main_menu)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
