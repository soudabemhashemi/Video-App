from django.utils.translation import gettext
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from video.models import Video


class WatchLaterAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    @staticmethod
    def post(request):
        data = request.data
        action = data.get('action')
        if action not in ['add', 'remove']:
            raise ValidationError({'action': _('Invalid action, choices are: (add, remove)')})

        video_code = data.get('video')
        if not video_code:
            raise ValidationError({'video': _('Video is required.')})

        try:
            video = Video.objects.get(code=video_code)
        except Video.DoesNotExist:
            raise ValidationError({'video': _('Video not found.')})

        channel = request.user.channel
        if action == 'add':
            success, _ = channel.watch_later_playlist.add_video(video=video)
            message = gettext('Added to watch later.')
        else:
            success, _ = channel.watch_later_playlist.remove_video(video=video)
            message = gettext('Removed from watch later.')

        if not success:
            raise ValidationError({'video': message})

        return Response({'success': success, 'message': message})
