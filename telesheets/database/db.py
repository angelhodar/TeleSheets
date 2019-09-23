import mongoengine as me
from telesheets.database.models import TelegramGroup
from telesheets.config import (
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_HOST
)

def connect():
    host = DB_HOST.replace('user', DB_USER).replace('password', DB_PASSWORD).replace('db_name', DB_NAME)
    me.connect(host=host)


def register_group(group_id):
    group = TelegramGroup(group_id=group_id)
    group.save()


def unregister_group(group_id):
    get_db_group(group_id).delete()


def get_db_group(group_id):
    try:
        return TelegramGroup.objects.get(group_id=group_id)
    except TelegramGroup.DoesNotExist:
        return None


def update_group_sheet(group_id, sheet_url):
    group = get_db_group(group_id)
    group.update(sheet_url=sheet_url)
    group.save()