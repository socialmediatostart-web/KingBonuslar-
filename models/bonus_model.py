from peewee import TextField, CharField, BooleanField
from models.base import BaseModel


class Bonus(BaseModel):
    description = TextField()
    photo_url = CharField(default='')
    group = CharField(default='')
    is_active = BooleanField(default=False)
    is_removed = BooleanField(default=False)
    is_request = BooleanField(default=True)
