import os

from django.conf import settings
from pytube import YouTube


class YoutubeService:
    DOWNLOAD_SUBDIR = 'crawled_videos/youtube/'

    @staticmethod
    def fetch_video_info(url):
        content = YouTube(url)
        info = {
            'link': content.watch_url,
            'title': content.title,
            'tags': content.keywords,
            'description': content.description,
            'publisher': content.channel_url,
            'thumbnail': content.thumbnail_url,
            'channel_name': content.author
        }
        return info

    @classmethod
    def download_video(cls, url):
        content = YouTube(url)
        download_path = os.path.join(settings.MEDIA_ROOT, cls.DOWNLOAD_SUBDIR)
        content.streams.filter(
            progressive=True, file_extension='mp4'
        ).order_by('resolution').desc().first().download(download_path)
