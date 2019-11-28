import json
from pygsheets import authorize
from telesheets.database import db
from telesheets.config import CREDENTIALS
from telesheets.config.sheets import IGNORED_HEADERS

gc = authorize(service_account_env_var="CREDENTIALS")

def get_client_email():
    return json.loads(CREDENTIALS)['client_email']


def get_worksheet(chat_id, wks_name):
    group = db.get_db_group(chat_id)
    sheet = group.sheet_url
    return gc.open_by_url(sheet).worksheet_by_title(wks_name)


def get_admin_ids(client, chat_id):
    admins = []
    for member in client.iter_chat_members(chat_id):
        if member.status in ['creator', 'administrator']:
            admins.append(member.user.id)
    return admins


def get_group_members(client, chat_id):
    members = {}
    for member in client.iter_chat_members(chat_id):
        members[member.user.username] = member.user.id
    return members


def row_to_message(row):
    return '\n'.join([f'{k}: {v}' for k, v in row.items()])


def worksheet_to_message(chat_id, worksheet_name):
    worksheet = get_worksheet(chat_id, worksheet_name)
    ignore_headers = IGNORED_HEADERS[worksheet_name]
    rows = worksheet.get_all_records(empty_value=None)
    filtered_rows = [filter_row(
        row, ignore_headers=ignore_headers) for row in rows]
    return '\n'.join([row_to_message(row) for row in filtered_rows])


def filter_row(row, ignore_headers=[]):
    filtered = {}
    for header, value in row.items():
        if header not in ignore_headers and value:
            filtered[header] = value
    return filtered


def iter_students(worksheet, group_members):
    rows = worksheet.get_all_records(empty_value=None)
    for row in rows:
        username = row['Telegram']
        if username in group_members.keys():
            student_id = group_members[username]
            data = filter_row(row)
            yield student_id, data


def notify(client, chat_id, worksheet_name, invoker):
    members = get_group_members(client, chat_id)
    worksheet = get_worksheet(chat_id, worksheet_name)
    notify_everyone = invoker in get_admin_ids(client, chat_id)
    for student_id, data in iter_students(worksheet, members):
        if notify_everyone:
            client.send_message(chat_id=student_id, text=row_to_message(data))
        elif student_id == invoker:
            client.send_message(chat_id=student_id, text=row_to_message(data))
            break
