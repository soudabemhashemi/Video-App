from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from user.services import VisitorService
from video.models import Video
from video.services import EventService


class PlayAPIView(APIView):

    class ReportSerializer(Serializer):
        video = CharField(max_length=10)
        time = IntegerField(min_value=0)

        @staticmethod
        def validate_video(value):
            try:
                video = Video.objects.get(code=value)
            except Video.DoesNotExist:
                raise ValidationError('video not found.')
            return video

    def post(self, request, *args, **kwargs):
        visitor_uuid = request.COOKIES.get(VisitorService.VISITOR_ID_KEY)
        serializer = self.ReportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            time = data['time']
            video = data['video']
            user = request.user if request.user.id else None
            EventService.log_watch(video=video, video_time=time, visitor_uuid=visitor_uuid, user=user)
            return Response({'success': True})
