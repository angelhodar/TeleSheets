import mongoengine as me

class TelegramGroup(me.Document):
    group_id = me.IntField(primary_key=True)
    sheet_url = me.StringField()

    meta = {'collection' : 'TelegramGroups'}