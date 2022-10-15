from uuid import uuid4

from django.db.models import UUIDField, ForeignKey, CASCADE, CharField

from _helpers.models import BaseModel


class Visitor(BaseModel):
    uuid = UUIDField(default=uuid4, unique=True)
    user = ForeignKey(to='auth.User', null=True, blank=True, related_name='visitors', on_delete=CASCADE)
    ip = CharField(null=True, blank=True, max_length=100)
    host = CharField(null=True, blank=True, max_length=200)
    user_agent = CharField(null=True, blank=True, max_length=1000)
