from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VideoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video'
    verbose_name = _('Video')
