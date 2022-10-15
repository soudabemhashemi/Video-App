from django.db.models import (Model, TextField, DateTimeField, ForeignKey, CASCADE)
from django.contrib.auth.models import User
from video.utils.convert_date import convert_date


class Comment(Model):
    text = TextField()
    sent_at = DateTimeField(auto_now_add=True)
    user = ForeignKey(to=User, on_delete=CASCADE)
    video = ForeignKey(to='Video', on_delete=CASCADE, related_name='comments')

    def __str__(self):
        return self.text

    def string_date(self):
        sent_at = convert_date(self.sent_at)
        return sent_at
