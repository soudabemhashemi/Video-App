from django.contrib import messages

from user.services import VisitorService
from video.mixin import CategoryMixinView
from video.models import Playlist
from video.models.comment import Comment
from django.views.generic.detail import DetailView
from video.models.video import Video
from video.serializers import CommentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from redis import StrictRedis
from video.models.report import ReportForm
from django.views.generic.edit import FormView
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from video.services import EventService

redis_client = StrictRedis(decode_responses=True)


class VideoView(CategoryMixinView, DetailView):
    model = Video
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_queryset(self):
        videos = Video.objects.filter(is_available=True, is_approved=True).\
            exclude(privacy=Video.PRIVACY_PRIVATE)
        user = self.request.user
        if user.id:
            users_videos = Video.objects.filter(channel=user.channel)
            videos = videos | users_videos
        return videos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = self.get_object()
        context['recommend'] = Video.objects.order_by('?')[:6]
        context['is_liked'] = video.is_liked_by_user(self.request.user.id)
        context['is_disliked'] = video.is_disliked_by_user(self.request.user.id)
        if self.request.user.id:
            is_added_to_watch_later = video.is_added_to_watch_later(self.request.user)
        else:
            is_added_to_watch_later = False
        context['is_added_to_watch_later'] = is_added_to_watch_later

        playlist_code = self.request.GET.get('playlist')
        if playlist_code:
            playlist = Playlist.objects.filter(code=playlist_code, channel=self.object.channel)
        else:
            playlist = None
        context['playlist'] = playlist
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        visitor_uuid = request.COOKIES.get(VisitorService.VISITOR_ID_KEY)
        video = self.get_object()
        user = request.user if request.user.id else None
        EventService.log_visit(video=video, visitor_uuid=visitor_uuid, user=user)
        return response


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        video = Video.objects.get(code=self.kwargs.get('code'))
        serializer.save(user=user, video=video)


class ReportFormView(FormView):
    form_class = ReportForm
    template_name = "video/play_video/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video'] = Video.objects.get(code=self.kwargs.get('code'))
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Form submission successful'))
        post = form.save(commit=False)
        post.user = self.request.user
        post.video = Video.objects.get(code=self.kwargs.get('code'))
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video:report', kwargs={'code': self.kwargs.get('code')})
