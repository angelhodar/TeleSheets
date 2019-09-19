import mongoengine as me

class GroupMember(me.EmbeddedDocument):
    user_id = me.IntField(primary_key=True)
    username = me.StringField(required=True)

class TelegramGroup(me.Document):
    group_id = me.IntField(primary_key=True)
    sheet_name = me.StringField(required=True)
    members = me.EmbeddedDocumentListField(GroupMember)

    meta = {'collection' : 'TelegramGroups'}