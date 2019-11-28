from loguru import logger
from pyrogram import Client, Filters
from telesheets.database import db
from telesheets.lib.utils import (
    get_client_email,
    worksheet_to_message,
    notify
)

from telesheets.lib.decorators import (
    validate_sheet,
    group_registered,
    restricted,
    bot_admin,
)

from telesheets.config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH
)

from telesheets.config.commands import (
    GROUP_COMMANDS,
    START,
    CONFIG,
    COMMANDS,
    SHEET,
    CHECK,
    EMAIL,
    CALENDAR,
    ATTENDANCE,
    GRADES
)

from telesheets.config.sheets import (
    GRADES_WKS_NAME,
    ATTENDANCE_WKS_NAME,
    CALENDAR_WKS_NAME
)

from telesheets.config.messages import (
    ONLY_GROUP_COMMAND_MSG,
    CONFIG_SUCCESSFUL_MSG,
    SHEET_UPDATED_MSG,
    GRADES_SENT_MSG,
    START_PRIVATE_MSG,
    START_GROUP_MSG,
    CONFIG_MSG,
    COMMANDS_LIST_MSG
)

# Initializes the bot
app = Client(":memory:", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH, bot_token=TELEGRAM_BOT_TOKEN)

@app.on_message(Filters.command(GROUP_COMMANDS) & Filters.private)
def on_wrong_chat_command(client, message):
    """
    Sends a message to the user that invokes a command in private
    chat that should only be invoked in groups
    """
    message.reply(ONLY_GROUP_COMMAND_MSG)


@app.on_message(Filters.command(START) & Filters.private)
def start_private(client, message):
    """
    Shows a start message for private conversations
    """
    logger.info('Sending start message to {}'.format(message.from_user.username))
    message.reply(START_PRIVATE_MSG)


@app.on_message(Filters.command(START) & Filters.group)
def start_group(client, message):
    """
    Shows a start message for private conversations
    """
    logger.info('Sending start message to group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=START_GROUP_MSG)


@app.on_message(Filters.command(CONFIG))
def config(client, message):
    """
    Shows a tutorial about how to link the group with Google Sheets.
    """
    logger.info('Sending config message to group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=CONFIG_MSG)


@app.on_message(Filters.command(COMMANDS))
def commands_list(client, message):
    """
    Shows all the available commands
    """
    logger.info('Sending commands list to {}'.format(message.from_user.username))
    client.send_message(chat_id=message.chat.id, text=COMMANDS_LIST_MSG)


@app.on_message(Filters.command(CHECK))
@restricted
@group_registered
@bot_admin
def check(client, message):
    """
    Shows if the group is correctly configured
    """
    logger.info('Sending configuration check to group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=CONFIG_SUCCESSFUL_MSG)
    message.delete()


@app.on_message(Filters.command(EMAIL))
def service_email(client, message):
    """
    Sends the email used to share the Google Sheet
    """
    logger.info('Email sent to {}'.format(message.from_user.username))
    client.send_message(chat_id=message.chat.id, text=get_client_email())


@app.on_message(Filters.command(SHEET))
@restricted
@bot_admin
@validate_sheet
def sheet(client, message):
    """
    Configures the Google Sheet for the group passing the url as parameter
    """
    sheet_url = message.command[1]
    db.update_group_sheet(message.chat.id, sheet_url)
    logger.info('Sheet updated for group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=SHEET_UPDATED_MSG)
    message.delete()


@app.on_message(Filters.command(CALENDAR))
@bot_admin
@group_registered
def calendar(client, message):
    """
    Shows the calendar wks in a group message
    """
    logger.info('Parsing calendar wks for group {}...'.format(message.chat.title))
    calendar = worksheet_to_message(message.chat_id, CALENDAR_WKS_NAME)
    client.send_message(chat_id=message.chat.id, text=calendar)
    logger.info('Calendar sent to group {}'.format(message.chat.title))
    message.delete()


@app.on_message(Filters.command(ATTENDANCE))
@bot_admin
@group_registered
def attendance(client, message):
    """
    Shows the attendance in private message for the requester member
    """
    logger.info('Parsing attendance for {}...'.format(message.from_user.username))
    notify(client, message.chat.id, ATTENDANCE_WKS_NAME, message.from_user.id)
    message.delete()
        

@app.on_message(Filters.command(GRADES))
@bot_admin
@group_registered
def grades(client, message):
    """
    Shows the grades in private message for each member
    """
    logger.info('Parsing grades wks for group {}...'.format(message.chat.title))
    notify(client, message.chat.id, GRADES_WKS_NAME, message.from_user.id)
    client.send_message(chat_id=message.chat.id, text=GRADES_SENT_MSG)
    message.delete()


@app.on_message(Filters.new_chat_members)
def on_enter_group(client, message):
    """
    Used to track when the bot is added to a new group
    """
    new_members = [member.id for member in message.new_chat_members]
    if client.get_me().id in new_members:
        db.register_group(message.chat.id)
        logger.info('New registered group: {}'.format(message.chat.title))
        client.send_message(chat_id=message.chat.id, text=START_GROUP_MSG)


@app.on_message(Filters.left_chat_member)
def on_leave_group(client, message):
    """
    Used to track when the bot is kicked from a group
    """
    if client.get_me().id == message.left_chat_member.id:
        db.unregister_group(message.chat.id)
        logger.info('Group {} unregistered'.format(message.chat.title))


if __name__ == "__main__":
    db.connect() # Connects to db using the environ database vars
    app.run() # Bot runs using start() and idle() to listen requests