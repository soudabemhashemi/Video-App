from django.db import transaction
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from video.models import Playlist, Video
from video.serializers import PlaylistSerializer, PlaylistEditSerializer


class PlaylistAPIView(ModelViewSet):
    lookup_field = "id"
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    queryset = Playlist.objects.all()


class PlaylistViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )
    lookup_field = 'code'
    lookup_url_kwarg = 'code'
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(channel__user=user)

    @action(methods=('post', ), detail=True)
    def edit(self, *args, **kwargs):
        playlist = self.get_object()
        data = self.request.data
        serializer = PlaylistEditSerializer(data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            success = True
            messages = []
            with transaction.atomic():
                for item in data:
                    _action = item['action']
                    video_code = item['video']
                    try:
                        video = Video.objects.get(code=video_code)
                    except Video.DoesNotExist:
                        success = False
                        messages.append({'video': f'Video {video_code} not found.'})
                        continue

                    if _action == 'add':
                        _success, _message = playlist.add_video(video)
                    elif _action == 'remove':
                        _success, _message = playlist.remove_video(video)
                    else:
                        order = item.get('order')
                        _success, _message = playlist.update_ordering(video, order)

                    success = success and _success
                    messages.append({'video': _message})

                if not success:
                    raise ValidationError({'success': success, 'messages': messages})

            return Response({'success': success, 'messages': messages})
