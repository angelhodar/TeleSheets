from telegram.ext import CommandHandler, MessageHandler, Filters
from utils import (
    get_wks,
    get_client_email,
    find_id_by_nick,
    parse_user_grades,
    validate_sheet,
    validate_chat_type,
    enough_privileges,
    bot_admin
)
from db import (
    validate_database_group,
    create_db_group,
    get_db_group,
    add_group_member,
    remove_group_member
)
from constants import(
    BOTNAME,
    CONFIG_MESSAGE,
    GROUP_CREATED,
    SHEET_UPDATED,
    CONFIG_SUCCESSFUL,
    COMMANDS_LIST
)


def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    message = '¡Hola! Escribe /config para empezar a enlazar este grupo con tu Google Sheet'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def config(update, context):
    """
    Shows a tutorial about how to link the group with Google Sheets
    """
    context.bot.send_message(chat_id=update.message.chat_id, text=CONFIG_MESSAGE)


def commands_list(update, context):
    """
    Shows all the available commands
    """
    context.bot.send_message(chat_id=update.message.chat_id, text=COMMANDS_LIST)


@validate_chat_type(['group', 'supergroup'])
@enough_privileges
@validate_database_group
@bot_admin
def check(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=CONFIG_SUCCESSFUL)
    update.message.delete()


def service_email(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=get_client_email())


@validate_chat_type(['group', 'supergroup'])
@enough_privileges
@validate_sheet
@bot_admin
def sheet(update, context):
    sheet_url = context.args[0]
    group = get_db_group(update.message.chat_id)
    if group:
        group.update(sheet_url=sheet_url)
        group.save()
    else:
        create_db_group(update.message.chat_id, sheet_url)
    
    message = SHEET_UPDATED if group else GROUP_CREATED
    context.bot.send_message(chat_id=update.message.chat_id, text=message)
    update.message.delete()


@bot_admin
@validate_chat_type(['group', 'supergroup'])
@validate_database_group
def calendar(update, context):
    message = 'No implementado todavia'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)
    update.message.delete()


@bot_admin
@validate_chat_type(['group', 'supergroup'])
@validate_database_group
def asistence(update, context):
    message = 'No implementado todavia'
    context.bot.send_message(chat_id=update.message.chat_id, text=message)
    update.message.delete()
        

@bot_admin
@validate_chat_type(['group', 'supergroup'])
@enough_privileges
@validate_database_group
def grades(update, context):
    """
    Shows the califications in private message for each user
    """
    group = get_db_group(update.message.chat_id)
    wks = get_wks(group.sheet_url)
    users = wks.get_all_records()
    for user in users:
        telegram_nick = user['Telegram']
        del user['Telegram']
        user_id = find_id_by_nick(telegram_nick, group.members)
        if user_id:
            context.bot.send_message(chat_id=user_id, text=parse_user_grades(user))
            
    context.bot.send_message(chat_id=update.message.chat_id, text='Todas las notas han sido enviadas!')
    update.message.delete()


@bot_admin
@validate_chat_type(['group', 'supergroup'])
@validate_database_group
def grade(update, context):
    group = get_db_group(update.message.chat_id)
    wks = get_wks(group.sheet_url)
    users = wks.get_all_records()
    sender = update.message.from_user.id
    for user in users:
        telegram_nick = user['Telegram']
        del user['Telegram']
        user_id = find_id_by_nick(telegram_nick, group.members)
        if user_id == sender:
            context.bot.send_message(chat_id=sender, text=parse_user_grades(user))
            break
    
    update.message.delete()


def unknown(update, context):
    """
    Executed when command is not implemented
    """
    update.message.reply_text("Lo siento, no reconozco ese comando")


def group_member_update(update, context):
    """
    Fires when a member joins/leaves the group
    """
    remove = True if update.message.left_chat_member else False
    if remove:
        remove_group_member(update.message.chat_id, update.message.left_chat_member)
    else:
        for member in update.message.new_chat_members:
            if member.username == BOTNAME:
                create_db_group(update.message.chat_id, sheet_url='Not asigned')
            else:
                add_group_member(update.message.chat_id, member)


# Handlers

# Basic Handlers
start_handler = CommandHandler('start', start)
config_handler = CommandHandler('config', config)
commands_list_handler = CommandHandler('comandos', commands_list)

# Configuration Handlers
sheet_handler = CommandHandler('hoja', sheet)
check_handler = CommandHandler('comprobar', check)
service_email_handler = CommandHandler('email', service_email)

# Data handlers
calendar_handler = CommandHandler('calendario', calendar)
asistence_handler = CommandHandler('asistencia', asistence)
grades_handler = CommandHandler('notas', grades)
grade_handler = CommandHandler('nota', grade)

# Other
status_handler = MessageHandler(Filters.status_update, group_member_update)
unknown_handler = MessageHandler(Filters.command, unknown)