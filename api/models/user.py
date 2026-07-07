from tortoise.models import Model
from tortoise.fields import CharField


class User(Model):
    id = CharField(max_length=50, pk=True)
    username = CharField(max_length=20, unique=True)
    email = CharField(max_length=300, unique=True)
    password = CharField(max_length=100)
