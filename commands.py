from models import TelegramGroup, GroupMember
from telegram.ext import CommandHandler, MessageHandler, Filters
from constants import (
    ONLY_ADMIN,
    ONLY_GROUPS,
    INVALID_SHEET
)
from utils import (
    wks_to_message,
    get_wks,
    validate_sheet,
    validate_chat_type,
    admin_executed,
    bot_admin
)

def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('¡Hola! Escribe /ayuda para ver todo en lo que te puedo ayudar')


@validate_sheet
@validate_chat_type
@admin_executed
@bot_admin
def config(update, context):
    group = TelegramGroup(group_id=update.message.chat_id, sheet_url=context.args[0])
    group.save()


@admin_executed
@bot_admin
@validate_chat_type
def spreadsheet(update, context):
    wks = get_wks('Test')
    message = wks_to_message(wks)
    update.message.reply_text(message)


def group_member_update(update, context):
    remove = True if update.message.left_chat_member else False
    member = update.message.left_chat_member if remove else update.message_new_chat_members[0]
    context.bot.send_message(chat_id=update.message.chat_id, text=member.username)
        

def unknown(update, context):
    """
    Executed when command is not implemented
    """
    update.message.reply_text("Lo siento, no reconozco ese comando")

# Handlers
start_handler = CommandHandler('start', start)
config_handler = CommandHandler('config', config)
sheet_handler = CommandHandler('hoja', spreadsheet)
status_handler = MessageHandler((Filters.status_update.new_chat_members & 
                                 Filters.status_update.left_chat_member), group_member_update)
unknown_handler = MessageHandler(Filters.command, unknown)