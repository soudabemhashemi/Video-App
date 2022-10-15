import urllib.parse

from django.db.models import Model, CharField, ForeignKey, CASCADE
from django.utils.translation import gettext_lazy as _


class VideoFormat(Model):

    video = ForeignKey(to='Video', on_delete=CASCADE, related_name='video_formats', verbose_name=_('Video'))

    _video_qualities = {
        1080: {
            'width': 1920, 'height': 1080, 'str': '1080p', 'resolution': '1920x1080',
            'bitrate': '5000k', 'max_bitrate': '5400k', 'buffer_size': '7500k',
            'audio_bitrate': '192k', 'bandwidth': '3500000'
        },
        720: {
            'width': 1280, 'height': 720, 'str': '720p', 'resolution': '1280x720',
            'bitrate': '2800k', 'max_bitrate': '3000k', 'buffer_size': '4200k',
            'audio_bitrate': '128k', 'bandwidth': '2000000'
        },
        480: {
            'width': 842, 'height': 480, 'str': '480p', 'resolution': '842x480',
            'bitrate': '1400k', 'max_bitrate': '1600k', 'buffer_size': '2100k',
            'audio_bitrate': '192k', 'bandwidth': '750000'
        },
        360: {
            'width': 640, 'height': 360, 'str': '360p', 'resolution': '640x360',
            'bitrate': '800k', 'max_bitrate': '1000k', 'buffer_size': '1200k',
            'audio_bitrate': '96k', 'bandwidth': '375000'
        },
        # 240: {
        #     'width': 426, 'height': 240, 'str': '240p', 'resolution': '426x240',
        #     'bitrate': '500k', 'max_bitrate': '600k', 'buffer_size': '750k',
        #     'audio_bitrate': '64k', 'bandwidth': '200000'
        # }
    }

    VIDEO_QUALITY_CHOICES = ((item['str'], item['str']) for item in _video_qualities.values())
    quality = CharField(choices=VIDEO_QUALITY_CHOICES, max_length=10, verbose_name=_('quality'))

    class Meta:
        verbose_name = _('Video format')
        verbose_name_plural = _('Video formats')

    @classmethod
    def get_video_qualities(cls):
        return cls._video_qualities

    @property
    def m3u8_url(self):
        return urllib.parse.urljoin(self.video.file.url, f'{self.video.video_file_name}/{self.quality}.m3u8')
