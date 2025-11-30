from rest_framework import generics
from .serializers import VideoSerializer, PodcastsSerializer
from sabuzz.models import Video, Podcasts

class VideoListAPI(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class PodcastsListAPI(generics.ListCreateAPIView):
    queryset = Podcasts.objects.all()
    serializer_class = PodcastsSerializer