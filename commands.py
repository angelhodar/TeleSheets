from models import TelegramGroup, GroupMember
from telegram.ext import CommandHandler, MessageHandler, Filters
from utils import (
    wks_to_message,
    get_wks,
    get_client_email,
    validate_sheet,
    validate_chat_type,
    admin_executed,
    bot_admin
)
from db import (
    validate_database_group,
    create_db_group,
    get_db_group,
    change_group_sheet,
    add_group_member,
    remove_group_member
)
from constants import(
    GROUP_CREATED,
    SHEET_UPDATED
)

def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('¡Hola! Escribe /ayuda para ver todo en lo que te puedo ayudar')


def help_func(update, context):
    """
    Shows a help message
    """
    message = 'Por construir'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


@admin_executed
@validate_chat_type
def check(update, context):
    pass


def service_email(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=get_client_email())


# @validate_sheet
@validate_chat_type
@admin_executed
@bot_admin
def sheet(update, context):
    sheet_name = ' '.join(context.args)
    # if get_db_group(update.message.chat_id):
    #     change_group_sheet(update.message.chat_id, sheet_name)
    #     update.message.reply_text(SHEET_UPDATED)
    # else:
    create_db_group(update.message.chat_id, sheet_name)
    update.message.reply_text(GROUP_CREATED)


@bot_admin
@validate_chat_type
@validate_database_group
def calendar(update, context):
    pass


@bot_admin
@validate_chat_type
@validate_database_group
def asistence(update, context):
    pass
        

@bot_admin
@validate_chat_type
@admin_executed
@validate_database_group
def califications(update, context):
    """
    Shows the califications
    """
    group = get_db_group(update.message.chat_id)
    wks = get_wks(group.sheet_name)
    message = wks_to_message(wks)
    update.message.reply_text(message)


@bot_admin
@validate_chat_type
@validate_database_group
def calification(update, context):
    pass


def unknown(update, context):
    """
    Executed when command is not implemented
    """
    update.message.reply_text("Lo siento, no reconozco ese comando")


def group_member_update(update, context):
    """
    Fires when a member joins/leaves the group
    """
    # context.bot.send_message(chat_id=update.message.chat_id, text='{} ha llegado'.format(update.message.new_chat_members[0].username))
    print('Hola')
    remove = True if update.message.left_chat_member else False
    member = update.message.left_chat_member if remove else update.message.new_chat_members[0]
    if remove:
        remove_group_member(update.message.chat_id, member)
    else:
        add_group_member(update.message.chat_id, member)


# Handlers

# Basic Handlers
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('ayuda', help_func)

# Configuration Handlers
sheet_handler = CommandHandler('hoja', sheet)
check_handler = CommandHandler('comprobar', check)
service_email_handler = CommandHandler('email', service_email)

# Data handlers
calendar_handler = CommandHandler('calendario', calendar)
asistence_handler = CommandHandler('asistencia', asistence)
califications_handler = CommandHandler('notas', califications)

# Other
status_handler = MessageHandler(Filters.status_update, group_member_update)
unknown_handler = MessageHandler(Filters.command, unknown)