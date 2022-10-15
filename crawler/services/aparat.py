import os.path
from bs4 import BeautifulSoup
import requests
import urllib.request
from django.conf import settings


class AparatService:
    DOWNLOAD_SUBDIR = 'crawled_videos/aparat/'

    @staticmethod
    def get_HTML_document(url):
        response = requests.get(url)
        return response.text

    @classmethod
    def fetch_post_info(cls, url):
        html_document = cls.get_HTML_document(url)
        soup = BeautifulSoup(html_document, 'html.parser')
        info = {
            'link': url,
            'title': soup.find('h1', attrs={'id': 'videoTitle'}).string,
            'description': soup.find('div', attrs={'class', 'description'}).text,
            'thumbnail': soup.find('meta', attrs={'property': "og:image"}).attrs.get('content'),
            'author': soup.find('a', attrs={'class', 'title'}).text
        }
        return info

    @classmethod
    def aparat_download_video(cls, url):
        html_document = cls.get_HTML_document(url)
        soup = BeautifulSoup(html_document, 'html.parser')
        video_name = f"{soup.find('h1', attrs={'id': 'videoTitle'}).string}.mp4"
        content = soup.find('div', attrs={'class': "download-dropdown"}).findAll('li', attrs={'class': 'menu-item-link link'})
        best_quality = content[-1]
        link = best_quality.find('a').attrs['href']
        download_path = os.path.join(settings.MEDIA_ROOT, cls.DOWNLOAD_SUBDIR)
        path = os.path.join(download_path, video_name)
        urllib.request.urlretrieve(link, path)
