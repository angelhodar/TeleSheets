import os
import mongoengine as me
from telegram.ext import Updater
from commands import (
    start_handler,
    config_handler,
    commands_list_handler,
    check_handler,
    sheet_handler, 
    status_handler,
    grades_handler,
    grade_handler,
    service_email_handler,
    unknown_handler
)
from extra_handlers import error

# Pipenv loads .env automatically, use dotenv module if not using pipenv
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']


if __name__ == "__main__":
    
    # Testing db
    me.connect('TeleSheets')

    # Gets the bot updater and dispatcher
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Main commands
    dp.add_handler(start_handler)
    dp.add_handler(config_handler)
    dp.add_handler(commands_list_handler)
    dp.add_handler(check_handler)
    dp.add_handler(sheet_handler)
    dp.add_handler(status_handler)
    dp.add_handler(grades_handler)
    dp.add_handler(grade_handler)
    dp.add_handler(service_email_handler)
    dp.add_handler(unknown_handler)

    # Logging error handler
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

