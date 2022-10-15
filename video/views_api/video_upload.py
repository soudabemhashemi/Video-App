from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from video.models import Video
from video.serializers import VideoSerializer


class UploadVideoAPIView(CreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Video.objects.filter(channel__user=self.request.user)

    def perform_create(self, serializer):
        channel = self.request.user.channel
        title = self.request.data.get('title')
        title = ".".join(title.split('.')[:-1])
        serializer.save(channel=channel, title=title)

