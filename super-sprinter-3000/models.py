from flaskr.connectdatabase import ConnectDatabase
from peewee import *


class Entries(Model):
    story_title = CharField()
    user_story = TextField()
    accepting_criteria = TextField()
    business_value = IntegerField()
    estimation = DecimalField()
    Status = CharField()

    class Meta:
        database = ConnectDatabase.db
