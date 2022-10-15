from django.db.models import Count
from django.views.generic.base import ContextMixin

from video.models import Category


class CategoryMixinView(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(v_count=Count('videos')).order_by('-v_count')
        context['categories'] = categories
        return context
