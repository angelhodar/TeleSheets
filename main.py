import mongoengine as me
from telegram.ext import Updater
from src.commands import (
    start_handler,
    config_handler,
    commands_list_handler,
    sheet_handler, 
    check_handler,
    service_email_handler,
    calendar_handler,
    asistence_handler,
    grades_handler,
    grade_handler,
    status_handler,
    unknown_handler
)
from src.extra_handlers import error
from src.config import TELEGRAM_TOKEN

def main():
    # Testing db
    me.connect('TeleSheets')

    # Gets the bot updater and dispatcher
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Main commands
    dp.add_handler(start_handler)
    dp.add_handler(config_handler)
    dp.add_handler(commands_list_handler)
    dp.add_handler(sheet_handler)
    dp.add_handler(check_handler)
    dp.add_handler(service_email_handler)
    dp.add_handler(calendar_handler)
    dp.add_handler(asistence_handler)
    dp.add_handler(grades_handler)
    dp.add_handler(grade_handler)
    dp.add_handler(status_handler)
    dp.add_handler(unknown_handler)

    # Logging error handler
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(clean=True)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":
    main()
    

