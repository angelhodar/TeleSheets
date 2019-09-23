import requests
from functools import wraps
from telesheets.lib.utils import get_admin_ids
from telesheets.database.db import get_db_group
from telesheets.database.models import TelegramGroup
from telesheets.config.constants import (
    NO_SHEET,
    URL_ERROR,
    INVALID_SHEET,
    COMMAND_ONLY_ADMINS,
    NO_BOT_ADMIN
)

def group_registered(func):
    @wraps(func)
    def wrapper(client, message, *args, **kwargs):
        group = get_db_group(message.chat.id)
        if group.sheet_url:
            return func(client, message, *args, **kwargs)
        else:
            message.reply(NO_SHEET)
    return wrapper


def validate_sheet(func):
    @wraps(func)
    def wrapper(client, message, *args, **kwargs):
        url = message.command[1]
        if 'docs.google.com/spreadsheets/d/' in url:
            try:
                requests.get(url).raise_for_status()
                return func(client, message, *args, **kwargs)
            except:
                message.reply(INVALID_SHEET)
        else:
            message.reply(URL_ERROR)

    return wrapper


def restricted(func):
    @wraps(func)
    def wrapper(client, message, *args, **kwargs):
        user = message.from_user.id
        if user in get_admin_ids(client, message.chat.id):
            return func(client, message, *args, **kwargs)
        else:
            message.reply(COMMAND_ONLY_ADMINS)
    return wrapper
    

def bot_admin(func):
    @wraps(func)
    def wrapper(client, message, *args, **kwargs):
        bot_id = client.get_me().id
        if bot_id in get_admin_ids(client, message.chat.id):
            return func(client, message, *args, **kwargs)
        else:
            message.reply(NO_BOT_ADMIN)
    return wrapper