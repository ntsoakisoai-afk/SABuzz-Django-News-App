from django.contrib import admin
<<<<<<< HEAD
from .models import Post, Category, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
=======
from .models import Post, Category, Comment, Profile, Like, Subscriber

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Subscriber)
>>>>>>> dev-backend
