from django.views.generic import TemplateView

from video.mixin import CategoryMixinView


class PolicyPageView(CategoryMixinView, TemplateView):
    template_name = 'video/policies/policy_page.html'
