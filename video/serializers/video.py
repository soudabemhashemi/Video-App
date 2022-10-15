from rest_framework.serializers import ModelSerializer

from video.models import Video


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'thumbnail', 'poster', 'file', 'code', 'description', 'category', 'is_visible', 'privacy')
