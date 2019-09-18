import pygsheets
from telegram.ext import CommandHandler

def wks_to_message(wks):
    message = ''
    sep = '----------------\n'
    data = wks.get_all_records()
    for record in data:
        for key, value in record.items():
            message += '{} : {}\n'.format(key, value)
        message += sep
    return message


def start(update, context):
    """
    Simple start command to introduce the bot functionality
    """
    update.message.reply_text('¡Hola! Escribe /ayuda para ver todo en lo que te puedo ayudar')

def spreadsheet(update, context):
    gc = pygsheets.authorize(service_file='creds.json')
    sheet_name = context.args[0]

    wks = gc.open(sheet_name).sheet1

    message = wks_to_message(wks)

    update.message.reply_text(message)



start_handler = CommandHandler('start', start)
sheet_handler = CommandHandler('hoja', spreadsheet)