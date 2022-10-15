from django.contrib.auth.models import User
from django.db.models import Model, CharField, OneToOneField, CASCADE, ForeignKey

from user.utils import validate_mobile_number, generate_verification_code


class Mobile(Model):
    number = CharField(max_length=11, validators=[validate_mobile_number], unique=True)
    user = OneToOneField(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} - {self.number}'

    @property
    def masked_number(self):
        return f'{self.number[:4]}-***-{self.number[-5:-1]}'
