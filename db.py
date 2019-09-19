from models import TelegramGroup, GroupMember
from constants import NO_DB_GROUP

def validate_database_group(func):
    def inner(update, context):
        try:
            get_db_group(update.message.chat_id)
            return func(update, context)
        except TelegramGroup.DoesNotExist:
            update.message.reply_text(NO_DB_GROUP)
    return inner


def create_db_group(group_id, sheet_name):
    group = TelegramGroup(group_id=group_id, sheet_name=sheet_name)
    group.save()


def get_db_group(group_id):
    return TelegramGroup.objects.get(group_id=group_id)


def change_group_sheet(group_id, sheet_name):
    get_db_group(group_id).update_one(sheet_name=sheet_name)


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