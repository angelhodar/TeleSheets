import mongoengine as me
from telesheets.database.models import TelegramGroup, GroupMember
from telesheets.config import (
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_HOST
)

def connect():
    host = DB_HOST.replace('user', DB_USER).replace('password', DB_PASSWORD).replace('db_name', DB_NAME)
    me.connect(host=host)


def create_db_group(group_id):
    group = TelegramGroup(group_id=group_id)
    group.save()


def get_db_group(group_id):
    try:
        return TelegramGroup.objects.get(group_id=group_id)
    except TelegramGroup.DoesNotExist:
        return None


def update_group_sheet(group_id, sheet_url):
    group = get_db_group(group_id)
    group.update(sheet_url=sheet_url)
    group.save()


def add_group_member(group_id, member):
    group_member = GroupMember(user_id=member.id, username=member.username)
    group = get_db_group(group_id)
    group.update(push__members=group_member)
    group.save()


def remove_group_member(group_id, member):
    group_member = GroupMember(user_id=member.id, username=member.username)
    group = get_db_group(group_id)
    group.update(pull__members=group_member)
    group.save()