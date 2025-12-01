from django.contrib import admin
from .models import Post, Category, Comment, Profile, Like, NewsletterSubscriber, Podcasts, Video

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    
admin.site.register(Profile, ProfileAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    seacrh_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'author', 'category')
    search_fields = ('title', 'author__username')
    ordering = ('created_at',)
    prepopulated_fields ={'slug': ('title',)}

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'date_posted', 'approved')
    list_filter = ('approved', 'date_posted')
    search_fields = ('user__username', 'post__title', 'text')

admin.site.register(Comment, CommentAdmin)

class LikeAdmin(admin.ModelAdmin):
    list_display =('post', 'user')
    search_fields = ('user__username', 'post__title')

admin.site.register(Like, LikeAdmin)

class NewsletterAdmin(admin.ModelAdmin):
    list_display =('email', 'subscribed_at')
    search_fields = ('email',)

admin.site.register(NewsletterSubscriber, NewsletterAdmin)


class PodcastsAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

admin.site.register(Podcasts, PodcastsAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

admin.site.register(Video, VideoAdmin)