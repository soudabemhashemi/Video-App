from django.urls import path

from video.views import HomePageView, SearchPageView, AboutPageView, PolicyPageView, \
    ContactUsFormView, WatchLaterPageView, HistoryPageView, LikedPageView, UploadPageView, EditVideoPageView, \
    MyVideosView, ChannelView, PlaylistView
from .views.video import VideoView, ReportFormView

app_name = 'video'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('result/', SearchPageView.as_view(), name='result'),
    path('upload/', UploadPageView.as_view(), name='upload_video'),
    path('watch_later/', WatchLaterPageView.as_view(), name='watch_later'),
    path('liked/', LikedPageView.as_view(), name='liked'),
    path('history/', HistoryPageView.as_view(), name='history'),
    path('myvideos/', MyVideosView.as_view(), name='my_videos'),
    path('playlist/<int:playlist_id>/', PlaylistView.as_view(), name='playlist'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('policy/', PolicyPageView.as_view(), name='policy'),
    path('contact_us/', ContactUsFormView.as_view(), name='contact_us'),
    path('video/<slug:code>/', VideoView.as_view(), name='video-detail'),
    path('video/edit/<slug:code>/', EditVideoPageView.as_view(), name='edit_video'),
    path('video/<slug:code>/report/', ReportFormView.as_view(), name='report'),
    path('channel/<slug:name>/', ChannelView.as_view(), name="channel-detail"),
]
