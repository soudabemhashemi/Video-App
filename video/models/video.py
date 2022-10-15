import os
import urllib.parse

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from _helpers.models import BaseModel

from video.utils.convert_date import convert_date
from video.utils import generate_video_code, FileSizeValidator
from redis import StrictRedis
from video.models.dislike import *
from django.utils.translation import ugettext_lazy as _
redis_client = StrictRedis(decode_responses=True)


KB = 1024
GB = 1024 * 1024 * 1024


class Video(BaseModel):

    channel = ForeignKey(to='Channel', on_delete=CASCADE, related_name='videos', verbose_name=_('Video|Channel'))
    code = models.CharField(max_length=8, default=generate_video_code, unique=True)
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Video|Title'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    category = models.ForeignKey(to='Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='videos', verbose_name=_('Category'))
    tags = models.ManyToManyField(to='Tag', blank=True, related_name='videos', verbose_name=_('Tags'))
    source = models.OneToOneField(to='CrawledVideo', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Source'))
    total_views = models.PositiveIntegerField(default=0)
    duration = models.DurationField(null=True, blank=True, verbose_name=_('Duration'))
    is_visible = models.BooleanField(default=False)
    PRIVACY_PUBLIC = 'PUBLIC'
    PRIVACY_UNLISTED = 'UNLISTED'
    PRIVACY_PRIVATE = 'PRIVATE'
    PRIVACY_CHOICES = (
        (PRIVACY_PUBLIC, PRIVACY_PUBLIC),
        (PRIVACY_UNLISTED, PRIVACY_UNLISTED),
        (PRIVACY_PRIVATE, PRIVACY_PRIVATE),
    )
    privacy = models.CharField(choices=PRIVACY_CHOICES, default=PRIVACY_PUBLIC, max_length=8, verbose_name=_('privacy'))
    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)

    VIDEOS_UPLOAD_TO_SUBDIR = 'video/videos/'
    POSTERS_UPLOAD_TO_SUBDIR = 'video/posters/'
    THUMBNAILS_UPLOAD_TO_SUBDIR = 'video/thumbnails/'

    file = models.FileField(
        upload_to=VIDEOS_UPLOAD_TO_SUBDIR,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'wmv', 'avi', 'flv', 'mkv']),
            FileSizeValidator(max_size=10 * GB)
        ],
        verbose_name=_('File')
    )

    thumbnail = models.ImageField(
        upload_to=THUMBNAILS_UPLOAD_TO_SUBDIR,
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']),
            FileSizeValidator(max_size=500 * KB)
        ],
        null=True,
        blank=True,
        verbose_name=_('Thumbnail')
    )
    poster = models.ImageField(
        upload_to=POSTERS_UPLOAD_TO_SUBDIR,
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']),
            FileSizeValidator(max_size=500 * KB)
        ],
        null=True,
        blank=True,
        verbose_name=_('Poster')
    )

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    @property
    def duration_str(self):
        if not self.duration:
            return None
        seconds = int(self.duration.total_seconds())
        output = str(self.duration).split('.')[0]
        if seconds >= 60:
            return output if output[0] != '0' else output[2:].lstrip('0')
        else:
            return f'0:{int(seconds)}'

    def __str__(self):
        return self.code

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_created = not self.id
        super(Video, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )
        if is_created:
            self.process_video()

    def is_liked_by_user(self, user_id):
        return self.likes.filter(user_id=user_id).exists()

    def is_disliked_by_user(self, user_id):
        return Dislike.objects.filter(video=self.id, user=user_id).exists()

    def is_added_to_watch_later(self, user):
        channel = user.channel
        return channel.watch_later_playlist.videos.filter(id=self.id).exists()

    def string_date(self):
        created_at = convert_date(self.created_at)
        return created_at

    @property
    def video_file_name(self):
        return os.path.splitext(os.path.basename(self.file.path))[0]

    @property
    def video_formats_dir_path(self):
        return os.path.splitext(self.file.path)[0]

    @property
    def video_master_file_url(self):
        return urllib.parse.urljoin(self.file.url, f'{self.video_file_name}/master.m3u8')

    def process_video(self):
        from video.tasks.video import process_video as process_video_task

        generate_thumbnail = not (self.thumbnail or self.poster)
        process_video_task.apply_async(args=(self.id, generate_thumbnail), queue='video')
