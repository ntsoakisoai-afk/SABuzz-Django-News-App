from django.urls import path
from .views import (
    VideoListAPI,
    PodcastListAPI,
)

urlpatterns = [
    path('videos/', VideoListAPI.as_view(), name='video_list'),
    path('podcasts/', PodcastListAPI.as_view(), name='podcast_list'),
]