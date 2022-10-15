from django.db.models import (Model, DateTimeField, ForeignKey, SET_NULL, TextField, EmailField, IntegerField)
from django.contrib.auth.models import User


class ContactUs(Model):
    user = ForeignKey(to=User, on_delete=SET_NULL, blank=True, null=True)
    name = TextField()
    email = EmailField()
    phone = IntegerField()
    created_at = DateTimeField(auto_now_add=True)
    description = TextField()
