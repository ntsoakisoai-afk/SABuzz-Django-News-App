from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Profile, Comment, Podcasts, Video

# ---------------------------
# User Signup Form
# ---------------------------
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


# ---------------------------
# User Login Form
# ---------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)


# ---------------------------
# Profile Form
# ---------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'profile_image']  # removed is_subscribed & subscription_date
        

# ---------------------------
# Post Form
# ---------------------------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


# ---------------------------
# Comment Form
# ---------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment here...'}),
        }


# ---------------------------
# Podcasts Form
# ---------------------------
class PodcastsForm(forms.ModelForm):
    class Meta:
        model = Podcasts
        fields = ['title', 'description', 'audio_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


# ---------------------------
# Video Form
# ---------------------------
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
