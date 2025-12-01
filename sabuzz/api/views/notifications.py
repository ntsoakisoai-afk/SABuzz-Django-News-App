from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from sabuzz.models import Notification
from sabuzz.api.serializers import NotificationSerializer

class AdminNotifications(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        return Response(NotificationSerializer(notifications, many=True).data)
