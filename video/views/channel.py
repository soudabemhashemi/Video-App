from django.views.generic import DetailView

from video.mixin import CategoryMixinView
from video.models import Channel


class ChannelView(CategoryMixinView, DetailView):
    model = Channel
    slug_field = 'name'
    slug_url_kwarg = 'name'
