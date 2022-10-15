from django.views.generic import TemplateView

from video.mixin import CategoryMixinView


class LikedPageView(CategoryMixinView, TemplateView):
    template_name = 'video/playlist/playlist_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked = self.request.user.channel.liked_playlist
        context['liked'] = True
        context['playlist'] = liked
        context['video_relations'] = liked.playlistvideorelation_set.order_by('order').all()
        return context
