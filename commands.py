import requests
from models import TelegramGroup, GroupMember
from telegram.ext import CommandHandler, MessageHandler, Filters
from utils import wks_to_message, get_wks

def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('¡Hola! Escribe /ayuda para ver todo en lo que te puedo ayudar')

def config(update, context):
    sheet_url = context.args[0]
    if not requests.get(sheet_url).raise_for_status():
        if update.message.chat.type == 'group':
            if update.message.from_user.id in [member.user.id for member in update.message.chat.get_administrators()]:
                group = TelegramGroup(group_id=update.message.chat_id, sheet_url=sheet_url)
                group.save()
            else:
                update.message.reply_text('Solo un administrador puede ejecutar este comando')
        else:
            update.message.reply_text('Este comando solo está disponible en los grupos')
    else:
        update.message.reply_text('El link a la hoja de google no es válido. Asegurate de copiarlo bien y vuelve a ejecutar el comando de nuevo')


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