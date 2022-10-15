from video.models.comment import Comment
from rest_framework import serializers
from django.contrib.auth.models import User
from video.utils.convert_date import convert_date
from video.models.channel import Channel
from video.models import Link
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', 'sent_at')

    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        data['channel'] = ChannelSerializer(instance=instance.user.channel).data
        data['sent_at'] = convert_date(instance.sent_at)
        return data


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ('avatar', 'title')


class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ('title', 'link')

    def validate(self, data):
        data = super(LinkSerializer, self).validate(attrs=data)
        if self.context.get('request').stream.method == 'POST':
            if Link.objects.filter(channel=self.context.get('request').user.channel, title=data.get('title')).count() > 0:
                raise serializers.ValidationError({'title': _("Your channel already has same type link.")})
            if Link.objects.filter(channel=self.context.get('request').user.channel, link=data.get('link')).count() > 0:
                raise serializers.ValidationError({'link': _("Your channel already has same link url.")})
        return data
