from django.db.models import BooleanField


from django.db.models import Model, CharField, URLField, IntegerField, ImageField, FileField
from django.utils.translation import ugettext_lazy as _

class CrawledVideo(Model):
    source = CharField(max_length=32)
    code = CharField(max_length=16)
    url = URLField(null=True, blank=True)
    download_url = URLField(null=True, blank=True)
    channel_name = CharField(max_length=64, default="")
    channel_url = URLField(null=True, blank=True)
    channel_verified = BooleanField(default=False)
    thumbnail_url = URLField(null=True, blank=True)
    views = IntegerField(default=0)
    likes = IntegerField(default=0)

    def __str__(self):
        return f'{self.url}'

    class Meta:
        verbose_name = _('Crawled video')
        verbose_name_plural = _('Crawled videos')
