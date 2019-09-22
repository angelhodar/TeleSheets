from telegram.ext import CommandHandler, MessageHandler, Filters
from telesheets.lib.decorators import (
    validate_database_group,
    validate_chat_type,
    validate_sheet,
    restricted,
    bot_admin,
)
from telesheets.lib.utils import (
    get_wks,
    get_client_email,
    find_id_by_nick,
    parse_calendar,
    notify
)
from telesheets.database.db import (
    create_db_group,
    get_db_group,
    update_group_sheet,
    add_group_member,
    remove_group_member
)
from telesheets.config.settings import (
    BOTNAME,
    GRADES_WKS_NAME,
    ASISTENCE_WKS_NAME,
    CALENDAR_WKS_NAME
)
from telesheets.config.messages import(
    START_PRIVATE,
    START_GROUP,
    CONFIG_MESSAGE,
    SHEET_UPDATED,
    CONFIG_SUCCESSFUL,
    COMMANDS_LIST,
    GRADES_SENT
)


def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    message = START_PRIVATE if update.message.chat.type == 'private' else START_GROUP
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
@restricted
@validate_database_group
@bot_admin
def check(update, context):
    """
    Tells admin if the group is correctly configured
    """
    context.bot.send_message(chat_id=update.message.chat_id, text=CONFIG_SUCCESSFUL)
    update.message.delete()


def service_email(update, context):
    """
    Sends the email used to share the Google Sheet
    """
    context.bot.send_message(chat_id=update.message.chat_id, text=get_client_email())


@validate_chat_type(['group', 'supergroup'])
@restricted
@validate_sheet
@bot_admin
def sheet(update, context):
    """
    Configures the Google Sheet for the group passing the url as parameter
    """
    sheet_url = context.args[0]
    update_group_sheet(update.message.chat_id, sheet_url)
    context.bot.send_message(chat_id=update.message.chat_id, text=SHEET_UPDATED)
    update.message.delete()


@bot_admin
@validate_chat_type(['group', 'supergroup'])
@validate_database_group
def calendar(update, context):
    group = get_db_group(update.message.chat_id)
    wks = get_wks(group.sheet_url, wks_name=GRADES_WKS_NAME)
    message = parse_calendar(wks)
    context.bot.send_message(chat_id=update.message.chat_id, text=message)
    update.message.delete()


@bot_admin
@validate_chat_type(['group', 'supergroup'])
@validate_database_group
def asistence(update, context):
    """
    Shows the asistence in private message for the requester member
    """
    group = get_db_group(update.message.chat_id)
    wks = get_wks(group.sheet_url, wks_name=ASISTENCE_WKS_NAME)
    requester = update.message.from_user.id
    notify(context.bot, group.members, wks, ignore_headers=['Telegram'], only_one=requester)
    update.message.delete()
        

@bot_admin
@validate_chat_type(['group', 'supergroup'])
@restricted
@validate_database_group
def grades(update, context):
    """
    Shows the califications in private message for each member
    """
    group = get_db_group(update.message.chat_id)
    wks = get_wks(group.sheet_url, wks_name=GRADES_WKS_NAME)
    notify(context.bot, group.members, wks, ignore_headers=['Telegram'])
    context.bot.send_message(chat_id=update.message.chat_id, text=GRADES_SENT)
    update.message.delete()


@bot_admin
@validate_chat_type(['group', 'supergroup'])
@validate_database_group
def grade(update, context):
    """
    Shows the califications in private message for the requester member
    """
    group = get_db_group(update.message.chat_id)
    wks = get_wks(group.sheet_url, wks_name=GRADES_WKS_NAME)
    requester = update.message.from_user.id
    notify(context.bot, group.members, wks, ignore_headers=['Telegram'], only_one=requester)
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
    if update.message.left_chat_member:
        remove_group_member(update.message.chat_id, update.message.left_chat_member)
    else:
        for member in update.message.new_chat_members:
            if member.username == BOTNAME:
                create_db_group(update.message.chat_id)
                message = START_PRIVATE if update.message.chat.type == 'private' else START_GROUP
                context.bot.send_message(chat_id=update.message.chat_id, text=message)
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