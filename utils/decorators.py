def info(func):
    def wrapper(*args, **kwargs):
        extracted_info = {}
        update = args[1]
        extracted_info['tg_id'] = update.effective_user.id
        extracted_info['chat_id'] = update.effective_chat.id
        extracted_info['message'] = update.effective_message
        extracted_info['callback'] = False
        if update.callback_query:
            extracted_info['callback'] = True
            extracted_info['data'] = update.callback_query.data.split()

        res = func(extracted_info, *args, **kwargs)

        if update.callback_query:
            update.callback_query.answer()

        return res
    return wrapper
