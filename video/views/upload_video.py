from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from video.mixin import CategoryMixinView


class UploadPageView(CategoryMixinView, LoginRequiredMixin, TemplateView):
    template_name = 'video/upload_video/upload_page.html'
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('video:upload_video')
