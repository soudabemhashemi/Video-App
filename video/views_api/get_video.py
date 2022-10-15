from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from video.models import Video


class GetVideoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        video_code = request.GET.get('video_code')
        try:
            video = Video.objects.get(code=video_code)
        except Video.DoesNotExist:
            raise ValidationError({'video': 'Video not found.'})
        return Response([{'title': video.title, 'thumbnail': video.thumbnail.url}], status=status.HTTP_200_OK)
