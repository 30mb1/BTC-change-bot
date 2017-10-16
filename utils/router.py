from wallet import wallet as w
from trade import trade as t
from admin import admin as a
from instruments import instruments as i
from utils.decorators import info

@info
def query_route(_, info, bot, update, user_data):
    if 'wallet' in info['data']:
        return w.query_route(bot, update, user_data=user_data)

    if 'trade' in info['data']:
        return t.query_route(bot, update, user_data=user_data)

    if 'admin' in info['data']:
        return a.query_route(bot, update, user_data=user_data)

    if 'settings' in info['data']:
        return i.query_route(bot, update, user_data=user_data)
