from django.urls import reverse_lazy
from django.views.generic import TemplateView

from video.mixin import CategoryMixinView


class WatchLaterPageView(CategoryMixinView, TemplateView):
    template_name = 'video/playlist/playlist_page.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        watch_later = self.request.user.channel.watch_later_playlist
        context['watch_later'] = True
        context['playlist'] = watch_later
        context['video_relations'] = watch_later.playlistvideorelation_set.order_by('order').all()
        return context
