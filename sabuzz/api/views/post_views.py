from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sabuzz.models import Post, Comment, Like
from sabuzz.api.serializers import PostSerializer, CommentSerializer
from sabuzz.permissions import IsAdmin, IsJournalist, IsUser

# ---------------------------
# List all published posts (Public / User)
# ---------------------------
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def get_queryset(self):
        return Post.objects.filter(status="published").order_by('-created_at')


# ---------------------------
# Retrieve single post details
# ---------------------------
class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsUser]
    queryset = Post.objects.filter(status="published")


# ---------------------------
# Create a post (Journalist / Admin)
# ---------------------------
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsJournalist]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ---------------------------
# Update a post (Journalist / Admin)
# ---------------------------
class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsJournalist]

    def get_queryset(self):
        # Journalists can update only their own posts
        return Post.objects.filter(author=self.request.user)


# ---------------------------
# Delete a post (Admin only)
# ---------------------------
class PostDeleteView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Post.objects.all()


# ---------------------------
# Comments for a post
# ---------------------------
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(user=self.request.user, post_id=post_id)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id, approved=True)


# ---------------------------
# Like / Unlike a post
# ---------------------------
class PostLikeToggle(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            # If already liked, unlike
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)
