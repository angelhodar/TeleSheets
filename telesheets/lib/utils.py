import json
from pygsheets import authorize
from telesheets.database import db
from telesheets.config import CREDENTIALS_PATH
from telesheets.config.constants import IGNORE_HEADERS


gc = authorize(service_account_file=CREDENTIALS_PATH)


def get_admin_ids(client, chat_id):
    admin_roles = ['creator', 'administrator']
    return [member.user.id for member in client.iter_chat_members(chat_id) if member.status in admin_roles]


def get_client_email():
    with open(CREDENTIALS_PATH) as json_file:
        email = json.load(json_file)['client_email']
    return email


def get_wks(chat_id, wks_name):
    group = db.get_db_group(chat_id)
    sheet = group.sheet_url
    return gc.open_by_url(sheet).worksheet_by_title(wks_name)


def find_id_by_nick(nick, members):
    try:
        return members[nick]
    except KeyError:
        return None

# TODO: Convert to generator
def get_students_data(wks_name, chat_id, telegram_members):
    wks = get_wks(chat_id, wks_name=wks_name)
    records = wks.get_all_records(empty_value=None)
    ignore_headers = IGNORE_HEADERS[wks_name]
    students = {}
    for record in records:
        student_id = find_id_by_nick(record['Telegram'], telegram_members)
        if student_id:
            students[student_id] = parse_record(record, ignore_headers)

    return students


def parse_record(row, ignore_headers=[]):
    return '\n'.join([f'{header} : {value}' for header, value in row.items() if header not in ignore_headers and value])


def parse_calendar(wks_name, chat_id):
    wks = get_wks(chat_id, wks_name=wks_name)
    events = wks.get_all_records(empty_value=None)
    calendar_message = '\n'.join([parse_record(event) for event in events])
    return calendar_message


# TODO: Add break
def parse_students(client, chat_id, wks_name, invoker):
    members = {m.user.username: m.user.id for m in client.iter_chat_members(chat_id)}
    notify_all = invoker in get_admin_ids(client, chat_id)
    students = get_students_data(wks_name, chat_id, members)
    for student, data in students.items():
        if invoker == student or notify_all:
            client.send_message(chat_id=student, text=data)
