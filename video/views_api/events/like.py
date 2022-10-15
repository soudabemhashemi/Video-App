from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from video.models import Video, Dislike, Like


class UpdateLikesDislikes(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, code):
        _type = request.data.get('type')
        video = Video.objects.get(code=code)
        user = request.user

        if _type == "like":
            data = self.like_video(video, user)
        elif _type == "dislike":
            data = self.dislike_video(video, user)
        else:
            raise ValidationError({'type': 'invalid type.'})
        return Response(data=data)

    @staticmethod
    def like_video(video, user):
        if video.is_disliked_by_user(user):
            Dislike.objects.get(video=video, user=user).delete()

        if video.is_liked_by_user(user):
            Like.objects.get(video=video, user=user).delete()
            is_increased = False
            video.channel.playlists.get(title='LL').remove_video(video)
        else:
            Like(video=video, user=user).save()
            is_increased = True
            video.channel.playlists.get(title='LL').add_video(video)
        if is_increased:
            message = _('Added to liked videos.')
        else:
            message = _('Removed from liked videos.')

        return {
            'dislike': video.dislikes.count(),
            'like': video.likes.count(),
            'is_increased': is_increased,
            'message': message
        }

    @staticmethod
    def dislike_video(video, user):
        if video.is_liked_by_user(user):
            Like.objects.get(video=video, user=user).delete()
            video.channel.playlists.get(title='LL').remove_video(video)
        if video.is_disliked_by_user(user):
            Dislike.objects.get(video=video, user=user).delete()
            is_increased = False
        else:
            Dislike(video=video, user=user).save()
            is_increased = True

        if is_increased:
            message = _('Added to disliked videos.')
        else:
            message = _('Removed from disliked videos.')

        return {
            'dislike': video.dislikes.count(),
            'like': video.likes.count(),
            'is_increased': is_increased,
            'message': message
        }
