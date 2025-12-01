# api/views/journalist_dashboard.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sabuzz.permissions import IsJournalist
from sabuzz.models import Post, Comment, Like
from api.serializers import PostSerializer

class JournalistDashboard(APIView):
    permission_classes = [IsAuthenticated, IsJournalist]

    def get(self, request):
        user = request.user
        data = {
            "total_articles": Post.objects.filter(author=user).count(),
            "published_articles": Post.objects.filter(author=user, status="published").count(),
            "drafts": Post.objects.filter(author=user, status="draft").count(),
            "total_comments": Comment.objects.filter(post__author=user).count(),
            "total_likes": Like.objects.filter(post__author=user).count(),
            "recent_articles": PostSerializer(Post.objects.filter(author=user).order_by('-created_at')[:5], many=True).data
        }
        return Response(data)
    
