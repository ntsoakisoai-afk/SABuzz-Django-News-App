from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from sabuzz.permissions import IsAdmin
from sabuzz.models import Post, Comment, Like, User, Profile

# Admin Dashboard Overview

class AdminDashboard(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        total_users = User.objects.count()
        total_journalists = Profile.objects.filter(role="journalist").count()
        total_posts = Post.objects.count()
        total_published_posts = Post.objects.filter(status="published").count()
        total_comments = Comment.objects.count()
        total_likes = Like.objects.count()

        recent_posts = Post.objects.order_by('-created_at')[:5].values(
            'id', 'title', 'author__username', 'status', 'created_at'
        )

        data = {
            "total_users": total_users,
            "total_journalists": total_journalists,
            "total_posts": total_posts,
            "total_published_posts": total_published_posts,
            "total_comments": total_comments,
            "total_likes": total_likes,
            "recent_posts": list(recent_posts),
        }
        return Response(data, status=status.HTTP_200_OK)

# Admin User Management

class AdminUserManagement(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all().values('id', 'username', 'email', 'profile__role')
        return Response({"users": list(users)}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            new_role = request.data.get('role')
            if new_role in ['admin', 'journalist', 'user']:
                user.profile.role = new_role
                user.profile.save()
                return Response({"detail": "User role updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class AdminApprovePost(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=404)
        post.status = "published"
        post.save()
        return Response({"detail": "Post approved."})

