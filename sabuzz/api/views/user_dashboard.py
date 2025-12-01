# api/views/user_dashboard.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sabuzz.permissions import IsUser, IsAdminOrJournalist
from sabuzz.models import Post, Podcasts, Video
from sabuzz.api.serializers import PostSerializer, PodcastSerializer, VideoSerializer

class UserDashboard(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        data = {
            "recent_posts": PostSerializer(Post.objects.filter(status="published").order_by('-created_at')[:5], many=True).data,
            "recent_podcasts": PodcastSerializer(Podcasts.objects.all().order_by('-uploaded_at')[:5], many=True).data,
            "recent_videos": VideoSerializer(Video.objects.all().order_by('-uploaded_at')[:5], many=True).data,
        }
        return Response(data)
class UserContentAccess(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrJournalist]

    def get(self, request):
        user = request.user
        data = {
            "all_posts": PostSerializer(Post.objects.filter(author=user), many=True).data,
            "all_podcasts": PodcastSerializer(Podcasts.objects.all(), many=True).data,
            "all_videos": VideoSerializer(Video.objects.all(), many=True).data,
        }
        return Response(data)

# User-specific content views
class UserPostList(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        posts = Post.objects.filter(status="published")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class UserPodcastList(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        podcasts = Podcasts.objects.all()
        serializer = PodcastSerializer(podcasts, many=True)
        return Response(serializer.data)

class UserVideoList(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


