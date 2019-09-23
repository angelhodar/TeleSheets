import json
from pygsheets import authorize
from telesheets.config import CREDENTIALS_PATH


gc = authorize(service_account_file=CREDENTIALS_PATH)


def get_admin_ids(client, chat_id):
    admin_roles = ['creator', 'administrator']
    return [admin.user.id for admin in client.iter_chat_members(chat_id) if admin.status in admin_roles]


def get_client_email():
    with open(CREDENTIALS_PATH) as json_file:
        email = json.load(json_file)['client_email']
    return email


def get_wks(sheet, wks_name):
    return gc.open_by_url(sheet).worksheet_by_title(wks_name)


def find_id_by_nick(nick, members):
    try:
        return members[nick]
    except KeyError:
        return None


def parse_row(row, ignore_headers=[]):
    message = ''
    valid_headers = [header for header in row if header not in ignore_headers]
    for header in valid_headers:
        # Only those ones not empty
        if row[header]:
            message += '{} : {}\n'.format(header, row[header])
    return message


def parse_calendar(wks):
    events = wks.get_all_records(empty_value=None)
    calendar_message = ''
    for event in events:
        calendar_message += '{}\n'.format(parse_row(event))
    return calendar_message


def notify(client, chat_id, wks, ignore_headers=[], only_one=None):
    students = wks.get_all_records(empty_value=None)
    members = {m.user.username : m.user.id for m in client.iter_chat_members(chat_id)}
    for student in students:
        student_id = find_id_by_nick(student['Telegram'], members)
        if only_one:
            if student_id == only_one:
                message = parse_row(student, ignore_headers=ignore_headers)
                client.send_message(chat_id=student_id, text=message)
                break
        else:
            message = parse_row(student, ignore_headers=ignore_headers)
            client.send_message(chat_id=student_id, text=message)