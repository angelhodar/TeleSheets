import requests
from pygsheets import authorize
from constants import (
    INVALID_SHEET,
    ONLY_GROUPS,
    ONLY_ADMIN,
    BOT_ADMIN
)

gc = None

def get_google_client():
    global gc
    gc = gc if gc else authorize(service_account_file='creds.json')
    return gc


def get_wks(sheet_name='Test'):
    return get_google_client().open_(sheet_name).sheet1

    
def wks_to_message(wks):
    message = ''
    sep = '----------------\n'
    data = wks.get_all_records()
    for record in data:
        for key, value in record.items():
            message += '{} : {}\n'.format(key, value)
        message += sep
    return message


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

