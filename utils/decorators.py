import texts
import gettext


LANGS = {
    'ru' : texts._,
    'en' : gettext.translation('messages', localedir='./locale', languages=['en']).gettext
}


def info(func):
    def wrapper(*args, **kwargs):

        # extracting useful data from update and pack it in a dictionary
        extracted_info = {}
        update = args[1]
        extracted_info['tg_id'] = update.effective_user.id
        extracted_info['chat_id'] = update.effective_chat.id
        extracted_info['message'] = update.effective_message
        extracted_info['callback'] = False

        if update.callback_query:
            extracted_info['callback'] = True
            extracted_info['data'] = update.callback_query.data.split()

        # determine user language and use appropriate translate function
        #print (kwargs, args)
        translation_func = LANGS[kwargs['user_data']['lang']]
        res = func(translation_func, extracted_info, *args, **kwargs)

        if update.callback_query:
            update.callback_query.answer()

        return res
    return wrapper
