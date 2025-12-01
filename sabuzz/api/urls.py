# api/urls.py
from django.urls import path
from api.views import admin_dashboard, journalist_dashboard, user_dashboard

urlpatterns = [
    # -------- Admin Dashboard --------
    path('admin/', admin_dashboard.AdminDashboard.as_view(), name='admin-dashboard'),
    path('admin/users/', admin_dashboard.AdminUserManagement.as_view(), name='admin-user-list'),
    path('admin/users/<int:user_id>/', admin_dashboard.AdminUserManagement.as_view(), name='admin-user-detail'),

    # -------- Journalist Dashboard --------
    path('journalist/', journalist_dashboard.JournalistDashboard.as_view(), name='journalist-dashboard'),
    path('journalist/create/', journalist_dashboard.JournalistCreatePost.as_view(), name='journalist-create-post'),
    path('journalist/update/<int:pk>/', journalist_dashboard.JournalistUpdatePost.as_view(), name='journalist-update-post'),
    path('journalist/drafts/', journalist_dashboard.JournalistDrafts.as_view(), name='journalist-drafts'),

    # -------- User Dashboard --------
    path('user/', user_dashboard.UserDashboard.as_view(), name='user-dashboard'),
    path('user/posts/', user_dashboard.UserPostList.as_view(), name='user-posts'),
    path('user/podcasts/', user_dashboard.UserPodcastList.as_view(), name='user-podcasts'),
    path('user/videos/', user_dashboard.UserVideoList.as_view(), name='user-videos'),
]
