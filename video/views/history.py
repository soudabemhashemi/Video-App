from django.views.generic import TemplateView

from video.mixin import CategoryMixinView


class HistoryPageView(CategoryMixinView, TemplateView):
    template_name = 'video/user_lists/user_lists_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = []
        return context
