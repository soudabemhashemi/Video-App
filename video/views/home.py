from django.views.generic import ListView

from video.models import Video
from video.mixin import CategoryMixinView


class HomePageView(CategoryMixinView, ListView):
    template_name = 'video/home/home_page.html'
    paginate_by = 40

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        videos = Video.objects.filter(is_available=True, is_approved=True, privacy=Video.PRIVACY_PUBLIC).order_by('-id')
        category = self.request.GET.get('cat')
        if category:
            videos = videos.filter(category_id=category)
        return videos
