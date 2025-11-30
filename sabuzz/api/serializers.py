from rest_framework import serializers
from sabuzz.models import Video, Podcasts

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class PodcastsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcasts
        fields = '__all__'