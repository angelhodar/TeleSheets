import mongoengine as me
from loguru import logger
from telesheets.database.models import TelegramGroup
from telesheets.config import (
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_HOST
)

def connect():
    host = DB_HOST.replace('user', DB_USER).replace('password', DB_PASSWORD).replace('db_name', DB_NAME)
    logger.info('Connecting to {}...'.format(host))
    me.connect(host=host)
    logger.info('Connected to database!')


def register_group(group_id):
    group = TelegramGroup(group_id=group_id)
    logger.info('Registering group with id {}...'.format(group_id))
    group.save()


def unregister_group(group_id):
    get_db_group(group_id).delete()
    logger.info('Unregistering group with id {}...'.format(group_id))


def get_db_group(group_id):
    try:
        return TelegramGroup.objects.get(group_id=group_id)
    except TelegramGroup.DoesNotExist:
        return None


def update_group_sheet(group_id, sheet_url):
    group = get_db_group(group_id)
    group.update(sheet_url=sheet_url)
    logger.info('Updating sheet with url {} on group id {}...'.format(sheet_url, group_id))
    group.save()