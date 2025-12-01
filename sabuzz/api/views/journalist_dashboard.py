# api/views/journalist_dashboard.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from sabuzz.permissions import IsJournalist
from sabuzz.models import Post, Comment, Like
from sabuzz.api.serializers import PostSerializer

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

class JournalistCreatePost(APIView):
    permission_classes = [IsAuthenticated, IsJournalist]
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JournalistUpdatePost(APIView):
    permission_classes = [IsAuthenticated, IsJournalist]
    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, author=request.user)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JournalistDrafts(APIView):
    permission_classes = [IsAuthenticated, IsJournalist]
    def get(self, request):
        drafts = Post.objects.filter(author=request.user, status="draft")
        serializer = PostSerializer(drafts, many=True)
        return Response(serializer.data)

class JournalistDeletePost(APIView):
    permission_classes = [IsAuthenticated, IsJournalist]
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, author=request.user)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
