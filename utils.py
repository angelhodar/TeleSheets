import os
import json
import requests
from pygsheets import authorize
from constants import (
    INVALID_SHEET,
    ONLY_GROUPS,
    ONLY_ADMIN,
    BOT_ADMIN
)

gc = authorize(service_account_file='creds.json')


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
    def inner(update, context):
        url = context.args[0]
        try:
            if not requests.get(url).raise_for_status():
                return func(update, context)
        except:
            update.message.reply_text(INVALID_SHEET)
    return inner


def validate_chat_type(func):
    def inner(update, context):
        if update.message.chat.type == 'group':
            return func(update, context)
        else:
            update.message.reply_text(ONLY_GROUPS)
    return inner


def admin_executed(func):
    def inner(update, context):
        sender = update.message.from_user.id
        admins = [member.user.id for member in update.message.chat.get_administrators()]
        if sender in admins:
            return func(update, context)
        else:
            update.message.reply_text(ONLY_ADMIN)
    return inner
    

def bot_admin(func):
    def inner(update, context):
        bot_id = context.bot.get_me().id
        admins = [member.user.id for member in update.message.chat.get_administrators()]
        if bot_id in admins:
            return func(update, context)
        else:
            update.message.reply_text(BOT_ADMIN)
    return inner
