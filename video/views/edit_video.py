from django.http import Http404, QueryDict
from django.views.generic import TemplateView

from video.mixin import CategoryMixinView
from video.models import Video, Tag


class EditVideoPageView(CategoryMixinView, TemplateView):

    def get_template_names(self):
        code = self.request.path.split('/')[-2]
        owner = Video.objects.get(code=code).channel.user
        if self.request.user == owner:
            return 'video/edit_video/edit_video_page.html'
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.request.path.split('/')[-2]
        video = Video.objects.filter(code=code)[0]
        context['video'] = video
        context['channel'] = self.request.user.channel
        context['tags'] = Tag.objects.all()
        return context
