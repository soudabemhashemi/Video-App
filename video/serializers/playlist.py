from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from video.models import Playlist


class PlaylistSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('code', 'title', 'channel', 'privacy', 'created_by')


class PlaylistEditSerializer(Serializer):
    ACTION_CHOICES = ('add', 'remove', 'move')
    action = ChoiceField(choices=ACTION_CHOICES)
    video = CharField(max_length=10)
    order = IntegerField(min_value=0, required=False)

    def validate(self, attrs):
        data = super().validate(attrs)
        if data['action'] == 'move':
            if data.get('order') is None:
                raise ValidationError({'order': 'order is required.'})
        return data
