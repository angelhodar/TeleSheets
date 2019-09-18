from telegram.ext import CommandHandler, MessageHandler, Filters
from utils import wks_to_message, get_google_client

def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('¡Hola! Escribe /ayuda para ver todo en lo que te puedo ayudar')

def spreadsheet(update, context):
    gc = get_google_client()
    sheet_name = context.args[0]
    wks = gc.open(sheet_name).sheet1
    message = wks_to_message(wks)
    update.message.reply_text(message)

def unknown(update, context):
    """
    Executed when command is not implemented
    """
    update.message.reply_text("Lo siento, no reconozco ese comando")


start_handler = CommandHandler('start', start)
sheet_handler = CommandHandler('hoja', spreadsheet)
unknown_handler = MessageHandler(Filters.command, unknown)