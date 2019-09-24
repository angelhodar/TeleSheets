from loguru import logger
from pyrogram import Client, Filters
from telesheets.database import db
from telesheets.lib.utils import (
    get_wks,
    get_client_email,
    parse_calendar,
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
from telesheets.config.constants import (
    START,
    CONFIG,
    COMMANDS,
    SHEET,
    CHECK,
    EMAIL,
    CALENDAR,
    ATTENDANCE,
    GRADE,
    GRADES,
    GRADES_WKS_NAME,
    ATTENDANCE_WKS_NAME,
    CALENDAR_WKS_NAME,
    GRADES_IGNORED_HEADERS,
    ATTENDANCE_IGNORED_HEADERS,
    CALENDAR_IGNORED_HEADERS,
    CONFIG_SUCCESSFUL,
    SHEET_UPDATED,
    GRADES_SENT,
    START_PRIVATE,
    START_GROUP,
    CONFIG_MESSAGE,
    COMMANDS_LIST
)


# Initializes the bot
app = Client("telesheets", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH, bot_token=TELEGRAM_BOT_TOKEN)


@app.on_message(Filters.command(START) & Filters.private)
def start_private(client, message):
    """
    Shows a start message for private conversations
    """
    logger.info('Sending start message to {}'.format(message.from_user.username))
    message.reply(START_PRIVATE)


@app.on_message(Filters.command(START) & Filters.group)
def start_group(client, message):
    """
    Shows a start message for groups
    """
    logger.info('Sending start message to group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=START_GROUP)


@app.on_message(Filters.command(CONFIG) & Filters.group)
def config(client, message):
    """
    Shows a tutorial about how to link the group with Google Sheets.
    """
    logger.info('Sending config message to group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=CONFIG_MESSAGE)


@app.on_message(Filters.command(COMMANDS))
def commands_list(client, message):
    """
    Shows all the available commands
    """
    logger.info('Sending commands list to {}'.format(message.from_user.username))
    client.send_message(chat_id=message.chat.id, text=COMMANDS_LIST)


@app.on_message(Filters.command(CHECK) & Filters.group)
@restricted
@group_registered
@bot_admin
def check(client, message):
    """
    Shows if the group is correctly configured
    """
    logger.info('Sending configuration check to group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=CONFIG_SUCCESSFUL)
    message.delete()


@app.on_message(Filters.command(EMAIL))
def service_email(client, message):
    """
    Sends the email used to share the Google Sheet
    """
    logger.info('Email sent to {}'.format(message.from_user.username))
    client.send_message(chat_id=message.chat.id, text=get_client_email())


@app.on_message(Filters.command(SHEET) & Filters.group)
@restricted
@validate_sheet
@bot_admin
def sheet(client, message):
    """
    Configures the Google Sheet for the group passing the url as parameter
    """
    sheet_url = message.command[1]
    db.update_group_sheet(message.chat.id, sheet_url)
    logger.info('Sheet updated for group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=SHEET_UPDATED)
    message.delete()


@app.on_message(Filters.command(CALENDAR) & Filters.group)
@bot_admin
@group_registered
def calendar(client, message):
    """
    Shows the calendar wks in a group message
    """
    logger.info('Parsing calendar wks for group {}...'.format(message.chat.title))
    group = db.get_db_group(message.chat.id)
    wks = get_wks(group.sheet_url, wks_name=CALENDAR_WKS_NAME)
    calendar_message = parse_calendar(wks)
    logger.info('Calendar sent to group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=calendar_message)
    message.delete()


@app.on_message(Filters.command(ATTENDANCE) & Filters.group)
@bot_admin
@group_registered
def attendance(client, message):
    """
    Shows the attendance in private message for the requester member
    """
    logger.info('Parsing attendance for {}...'.format(message.from_user.username))
    group = db.get_db_group(message.chat.id)
    wks = get_wks(group.sheet_url, wks_name=ATTENDANCE_WKS_NAME)
    requester = message.from_user.id
    logger.info('Attendance data sent to {}'.format(message.from_user.username))
    notify(client, message.chat.id, wks, ignore_headers=ATTENDANCE_IGNORED_HEADERS, only_one=requester)
    message.delete()
        

@app.on_message(Filters.command(GRADES) & Filters.group)
@bot_admin
@restricted
@group_registered
def grades(client, message):
    """
    Shows the grades in private message for each member
    """
    logger.info('Parsing grades wks for group {}...'.format(message.chat.title))
    group = db.get_db_group(message.chat.id)
    wks = get_wks(group.sheet_url, wks_name=GRADES_WKS_NAME)
    notify(client, message.chat.id, wks, ignore_headers=GRADES_IGNORED_HEADERS)
    logger.info('Grades sent for group {}'.format(message.chat.title))
    client.send_message(chat_id=message.chat.id, text=GRADES_SENT)
    message.delete()


@app.on_message(Filters.command(GRADE) & Filters.group)
@bot_admin
@group_registered
def grade(client, message):
    """
    Shows the grade in private message for the requester member
    """
    group = db.get_db_group(message.chat_id)
    wks = get_wks(group.sheet_url, wks_name=GRADES_WKS_NAME)
    requester = message.from_user.id
    notify(client, message.chat.id, wks, ignore_headers=GRADES_IGNORED_HEADERS, only_one=requester)
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
        client.send_message(chat_id=message.chat.id, text=START_GROUP)


@app.on_message(Filters.left_chat_member)
def on_leave_group(client, message):
    """
    Used to track when the bot is kicked from a group
    """
    if client.get_me().id == message.left_chat_member.id:
        db.unregister_group(message.chat.id)
        logger.info('Group {} unregistered'.format(message.chat.title))



if __name__ == "__main__":
    # Connects to db using the environ database vars
    db.connect()
    # Bot runs using start() and idle() to listen requests (4 threads)
    app.run()