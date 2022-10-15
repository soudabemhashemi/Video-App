from datetime import timedelta

from django.views.generic import ListView

from video.mixin import CategoryMixinView
from video.models import Video


class SearchPageView(CategoryMixinView, ListView):
    template_name = 'video/search/search_page.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        videos = self.dummy_search()
        videos = self.filter_video_result(videos)
        return videos

    def filter_video_result(self, videos):
        filtered_duration = self.request.GET.get('dur')
        filtered_order = self.request.GET.get('order')
        if filtered_duration != '0':
            if filtered_duration == '1':  # under 5min
                return videos.filter(duration__lte=timedelta(minutes=5))
            elif filtered_duration == '2':  # 5-20 min
                return videos.filter(duration__gt=timedelta(minutes=5), duration__lte=timedelta(minutes=20))
            elif filtered_duration == '3':  # over 20 min
                return videos.filter(duration__gt=timedelta(minutes=20))
        if filtered_order != '0':
            if filtered_order == '1':  # newest
                return videos.order_by('-created_at')
            elif filtered_order == '2':  # oldest
                return videos.order_by('created_at')
            elif filtered_order == '3':  # most views
                return videos.order_by('-total_views')
            elif filtered_order == '4':  # least views
                return videos.order_by('total_views')
        return videos

    def dummy_search(self):
        search_input = self.request.GET.get('in')
        if search_input:
            by_title = Video.objects.filter(title__icontains=search_input)
            by_channel_name = Video.objects.filter(channel__name__icontains=search_input)
            by_description = Video.objects.filter(description__icontains=search_input)
            return (by_title | by_channel_name | by_description).distinct()
        else:
            return Video.objects.all()
