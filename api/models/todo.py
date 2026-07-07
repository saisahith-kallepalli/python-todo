from tortoise.models import Model
from tortoise.fields import CharField, IntField, BooleanField


class Todo(Model):
    id = IntField(pk=True)
    title = CharField(max_length=100, null=False)
    description = CharField(max_length=200)
    done = BooleanField(default=False)
    userId = CharField(max_length=50)
