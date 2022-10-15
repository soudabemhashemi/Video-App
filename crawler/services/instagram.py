import os

from django.conf import settings
from instalooter.looters import PostLooter


class InstagramService:
    DOWNLOAD_SUBDIR = 'crawled_videos/instagram/'

    @staticmethod
    def fetch_post_info(url):
        content = PostLooter(url)
        info = {
            'link': url,
            'description': content.info['edge_media_to_caption'].get('edges')[0].get('node').get('text'),
            'thumbnail': content.info['thumbnail_src'],
            'author': content.info.get('owner').get('username')}
        return info

    @classmethod
    def instagram_download_video(cls, url):
        content = PostLooter(url)
        download_path = os.path.join(settings.MEDIA_ROOT, cls.DOWNLOAD_SUBDIR)
        content.download_videos(download_path)
