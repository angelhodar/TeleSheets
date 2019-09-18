from telegram.ext import CommandHandler, MessageHandler, Filters
from utils import wks_to_message, get_google_client

def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('¡Hola! Escribe /ayuda para ver todo en lo que te puedo ayudar')

def spreadsheet(update, context):
    gc = get_google_client()
    wks = gc.open('Test').sheet1
    message = wks_to_message(wks)
    update.message.reply_text(message)

def unknown(update, context):
    """
    Executed when command is not implemented
    """
    update.message.reply_text("Lo siento, no reconozco ese comando")

def insert(update, context):
    gc = get_google_client()
    wks = gc.open('Test').sheet1
    wks.update_values(context.args[0], [['Pepe Viyuela'], [5], [6]], majordim='COLUMNS')
    update.message.reply_text('Hoja actualizada')


start_handler = CommandHandler('start', start)
sheet_handler = CommandHandler('hoja', spreadsheet)
insert_handler = CommandHandler('insertar', insert)
unknown_handler = MessageHandler(Filters.command, unknown)