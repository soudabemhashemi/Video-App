from django.db.models import (Model, DateTimeField, ForeignKey, CASCADE)
from django.contrib.auth.models import User


class Dislike(Model):
    user = ForeignKey(to=User, on_delete=CASCADE)
    video = ForeignKey(to='Video', on_delete=CASCADE, related_name='dislikes')
    acted_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "video")
