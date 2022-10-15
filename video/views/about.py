from django.views.generic import TemplateView

from video.mixin import CategoryMixinView


class AboutPageView(CategoryMixinView, TemplateView):
    template_name = 'video/about/about_page.html'
