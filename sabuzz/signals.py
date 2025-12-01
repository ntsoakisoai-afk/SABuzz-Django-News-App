from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from sabuzz.models import Profile, Post, Comment, Like, Podcasts, Video, Notification

#Create Profile automatically when a User is created

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save Profile automatically when a User is saved

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Helper to send notification to all admins

def notify_admins(title, message, notif_type):
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        Notification.objects.create(
            user=admin,
            notif_type=notif_type,
            title=title,
            message=message
        )


#New Post

@receiver(post_save, sender=Post)
def notify_admin_new_post(sender, instance, created, **kwargs):
    if created and instance.status == "pending":
        notify_admins(
            title=f"New Post Awaiting Approval",
            message=f"'{instance.title}' by {instance.author.username} is waiting for review.",
            notif_type='post'
        )


#Post Updated

@receiver(post_save, sender=Post)
def notify_admin_updated_post(sender, instance, created, **kwargs):
    if not created and instance.status == "pending":
        notify_admins(
            title=f"Post Updated",
            message=f"The post '{instance.title}' was updated and needs re-review.",
            notif_type='post'
        )


#New Comment

@receiver(post_save, sender=Comment)
def notify_admin_new_comment(sender, instance, created, **kwargs):
    if created:
        notify_admins(
            title="New Comment Added",
            message=f"A new comment by {instance.author.username} on '{instance.post.title}'.",
            notif_type='comment'
        )


#New Like

@receiver(post_save, sender=Like)
def notify_admin_new_like(sender, instance, created, **kwargs):
    if created:
        notify_admins(
            title="New Post Like",
            message=f"{instance.user.username} liked '{instance.post.title}'.",
            notif_type='like'
        )


#New Podcast

@receiver(post_save, sender=Podcasts)
def notify_admin_new_podcast(sender, instance, created, **kwargs):
    if created:
        notify_admins(
            title="New Podcast Uploaded",
            message=f"Podcast '{instance.title}' was uploaded by {instance.author.username}.",
            notif_type='podcast'
        )


#New Video
@receiver(post_save, sender=Video)
def notify_admin_new_video(sender, instance, created, **kwargs):
    if created:
        notify_admins(
            title="New Video Uploaded",
            message=f"Video '{instance.title}' was uploaded.",
            notif_type='video'
        )
