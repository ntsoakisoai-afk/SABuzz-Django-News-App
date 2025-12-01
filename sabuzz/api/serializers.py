from rest_framework import serializers
from sabuzz.models import Post, Comment, Like, Podcasts, Video, Profile, Notification

# Profile Serializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'role', 'profile_image']

# Post Serializer

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'category',
            'author',
            'author_username',
            'image',
            'status',
            'source',
            'views',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['slug', 'author', 'views', 'created_at', 'updated_at']


# Comment Serializer

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'user',
            'user_username',
            'text',
            'date_posted',
            'approved',
        ]
        read_only_fields = ['user', 'date_posted', 'approved']

# Like Serializer

class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'post', 'post_title', 'user', 'user_username']
        read_only_fields = ['user']

# Podcast Serializer

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcasts
        fields = ['id', 'title', 'description', 'audio_file', 'uploaded_at']

# Video Serializer

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'uploaded_at']

#Notification Serializer

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'