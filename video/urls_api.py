from django.urls import path, include
from rest_framework.routers import DefaultRouter

from video.views_api import UploadVideoAPIView, EditVideoAPIView, SubscriptionAPIView, UnsubscriptionAPIView, \
    PlayAPIView, UpdateLikesDislikes, WatchLaterAPIView, GetVideoAPIView, PlaylistAPIView, \
    PlaylistViewSet, LinkViewSet
from .views.video import CommentViewSet

app_name = 'video-api'

router = DefaultRouter()
router.register('playlists', PlaylistViewSet, basename='playlist')

urlpatterns = [
    path('channel/<int:pk>/subscribe/', SubscriptionAPIView.as_view(), name='subscribe_api'),
    path('channel/<int:pk>/unsubscribe/', UnsubscriptionAPIView.as_view(), name='unsubscribe_api'),
    path('api/upload/video/', UploadVideoAPIView.as_view(), name='upload_video_api'),
    path('api/edit/video/<slug:code>/', EditVideoAPIView.as_view({'patch': 'partial_update', 'get': 'retrieve'}), name='edit_video_api'),
    path('video/<slug:code>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comments'),
    path('video/<slug:code>/like-dislike/', UpdateLikesDislikes.as_view(), name='like_or_dislike'),
    path('watch-later/', WatchLaterAPIView.as_view(), name='watch-later'),
    path('get-video/', GetVideoAPIView.as_view(), name='get-video'),
    path('links/<int:pk>/', LinkViewSet.as_view({'delete': 'destroy', 'post': 'create', 'put': 'update'}), name='links'),

    path('get-video/', GetVideoAPIView.as_view(), name='get-video'),
    path('playlist/<int:id>/edit', PlaylistAPIView.as_view({'patch': 'partial_update'}), name='playlists_api'),
    path('', include(router.urls)),

    path('reports/play/', PlayAPIView.as_view(), name='report-play'),
]
