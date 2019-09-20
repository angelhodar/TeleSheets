import os
import json
import requests
from pygsheets import authorize
from functools import wraps
from constants import (
    INVALID_SHEET,
    URL_ERROR,
    ONLY_GROUPS,
    ONLY_ADMIN,
    BOT_ADMIN,
    SHEET_URL_FORMAT
)

gc = authorize(service_account_file='creds.json')


def is_valid_url_domain(url):
    return SHEET_URL_FORMAT in url


def get_admin_ids(chat):
    return [admin.user.id for admin in chat.get_administrators()]


def get_client_email():
    with open(os.environ['CREDENTIALS_PATH']) as json_file:
        email = json.load(json_file)['client_email']
    return email


def get_wks(sheet, wks_name='Notas'):
    return gc.open_by_url(sheet).worksheet_by_title(wks_name)


def parse_user_grades(data):
    string = ''
    for key, value in data.items():
        string += '{} : {}\n'.format(key, value)
    return string


def find_id_by_nick(nick, members):
    for m in members:
        if m.username == nick:
            return m.user_id
    return None


# Decorators
def validate_sheet(func):
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        url = context.args[0]
        if is_valid_url_domain(url):
            try:
                requests.get(url).raise_for_status()
                return func(update, context, *args, **kwargs)
            except:
                update.message.reply_text(URL_ERROR)
        else:
            update.message.reply_text(INVALID_SHEET)

    return wrapper


def validate_chat_type(allowed_types):
    def decorator(func):
        @wraps(func)
        def wrapper(update, context, *args, **kwargs):
            if update.message.chat.type in allowed_types:
                return func(update, context, *args, **kwargs)
            else:
                update.message.reply_text(ONLY_GROUPS)
        return wrapper
    return decorator


def enough_privileges(func):
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        user = update.message.from_user.id
        if user in get_admin_ids(update.message.chat):
            return func(update, context, *args, **kwargs)
        else:
            update.message.reply_text(ONLY_ADMIN)
    return wrapper
    

def bot_admin(func):
    @wraps(func)
    def wrapper(update, context, *args, **kwargs):
        bot_id = context.bot.get_me().id
        if bot_id in get_admin_ids(update.message.chat):
            return func(update, context, *args, **kwargs)
        else:
            update.message.reply_text(BOT_ADMIN)
    return wrapper
