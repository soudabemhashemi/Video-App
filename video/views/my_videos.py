from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from video.mixin import CategoryMixinView
from video.models import Video


class MyVideosView(CategoryMixinView, LoginRequiredMixin, TemplateView):
    template_name = 'video/my_videos/my_videos_page.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.request.user
        context['videos'] = Video.objects.filter(channel__user=owner).order_by('-created_at')
        return context
