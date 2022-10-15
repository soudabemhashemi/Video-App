from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from video.mixin import CategoryMixinView
from video.models import Playlist


class PlaylistView(CategoryMixinView, LoginRequiredMixin, TemplateView):
    template_name = 'video/playlist/playlist_page.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, playlist_id, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = Playlist.objects.get(id=playlist_id)
        context['playlist'] = playlist
        context['video_relations'] = playlist.playlistvideorelation_set.order_by('order').all()
        return context
