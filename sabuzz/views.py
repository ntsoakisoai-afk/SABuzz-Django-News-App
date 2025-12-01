import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login  # ensure this import is at top of views.py
from .models import (
    Post, Category, Comment, Subscriber,
    Favorite, SavedArticle, SavedPost
)

API_KEY = "pub_5741e9332f0f408186a23f2be286c5f5"


# ============================================================
# JOURNALIST / ADMIN ONLY CHECK
# ============================================================
def is_journalist(user):
    return user.is_superuser or user.groups.filter(name="Journalists").exists()


# ============================================================
# HOME PAGE – API NEWS
# ============================================================
def home(request):
    url = f"https://newsdata.io/api/1/news?country=za&apikey={API_KEY}"
    articles = []

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        articles = data.get("results", [])
    except Exception:
        articles = []

    return render(request, "sabuzz/index.html", {"articles": articles})


# ============================================================
# WEATHER PAGE
# ============================================================
def weather_widget(request):
    lat = -26.2041
    lon = 28.0473

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
        f"&timezone=Africa/Johannesburg"
    )

    weather = {}
    forecast = []

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        weather = data.get("current_weather", {})
        daily = data.get("daily", {})

        forecast = zip(
            daily.get("time", []),
            daily.get("temperature_2m_min", []),
            daily.get("temperature_2m_max", []),
            daily.get("weathercode", []),
        )
    except Exception:
        pass

    return render(request, "sabuzz/weather.html", {
        "weather": weather,
        "forecast": forecast
    })


# ============================================================
# LOGIN
# ============================================================
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "sabuzz/login.html")


# ============================================================
# LOGOUT (redirect to HOME)
# ============================================================
def logout_user(request):
    logout(request)
    return redirect("home")


# ============================================================
# STATIC PAGES
# ============================================================
def about(request):
    return render(request, "sabuzz/about.html")

def contact(request):
    return render(request, "sabuzz/contact.html")


# ============================================================
# DASHBOARD (Journalist/Admin Only)
# ============================================================
@user_passes_test(is_journalist)
def dashboard(request):
    posts = Post.objects.all()

    context = {
        "posts_count": posts.count(),
        "categories_count": Category.objects.count(),
        "subscribers_count": Subscriber.objects.count(),
        "comments_count": Comment.objects.count(),
        "total_views": sum(getattr(p, "views", 0) for p in posts),
    }

    return render(request, "sabuzz/dashboard.html", context)


# ============================================================
# SUBSCRIBERS LIST
# ============================================================
@user_passes_test(is_journalist)
def subscribers_list(request):
    subscribers = Subscriber.objects.all().order_by("-subscribed_at")
    return render(request, "sabuzz/subscribers_list.html", {
        "subscribers": subscribers
    })


# ============================================================
# CATEGORY PAGE
# ============================================================
def category_news(request, category):
    url = f"https://newsdata.io/api/1/news?country=za&category={category}&apikey={API_KEY}"
    articles = []

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        articles = data.get("results", [])
    except Exception:
        articles = []

    return render(request, "sabuzz/category.html", {
        "category": category.capitalize(),
        "articles": articles
    })


# ============================================================
# SEARCH PAGE
# ============================================================
def search_news(request):
    query = request.GET.get("q", "")
    url = f"https://newsdata.io/api/1/news?q={query}&country=za&apikey={API_KEY}"
    articles = []

    if query:
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            articles = data.get("results", [])
        except Exception:
            articles = []

    return render(request, "sabuzz/search.html", {
        "query": query,
        "articles": articles
    })


# ============================================================
# FAVORITE API NEWS (requires login)
# ============================================================
@login_required
def save_favorite(request):
    Favorite.objects.create(
        user=request.user,
        title=request.POST.get("title"),
        link=request.POST.get("link"),
        image_url=request.POST.get("image_url"),
        source=request.POST.get("source")
    )
    return redirect("favorites")


@login_required
def favorites(request):
    saved = Favorite.objects.filter(user=request.user).order_by("-saved_at")
    return render(request, "sabuzz/favorites.html", {"saved": saved})


# ============================================================
# SAVED API ARTICLES (AUTH CHOICE only)
# ============================================================
def save_article(request):
    if not request.user.is_authenticated:
        return render(request, "sabuzz/auth_choice.html")

    if request.method == "POST":
        SavedArticle.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            url=request.POST.get("url"),
            image_url=request.POST.get("image_url"),
            source_name=request.POST.get("source_name")
        )

    return redirect("saved_articles")


@login_required
def saved_articles(request):
    saved = SavedArticle.objects.filter(user=request.user)
    return render(request, "sabuzz/saved_articles.html", {"saved": saved})


# ============================================================
# REGISTER (AUTO-LOGIN + REDIRECT TO DASHBOARD)
# ============================================================


def register_user(request):
    """
    Create account, auto-login the new user, show success message,
    then redirect to the site home page (not the journalist dashboard).
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # auto-login
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("home")  # <- send normal users to home
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserCreationForm()

    return render(request, "sabuzz/register.html", {"form": form})


# ============================================================
# POST DETAIL PAGE (LOCAL POSTS)
# ============================================================
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "sabuzz/post_detail.html", {"post": post})


# ============================================================
# SAVE LOCAL POST (AUTH CHOICE)
# ============================================================
def save_post(request, post_id):
    if not request.user.is_authenticated:
        return render(request, "sabuzz/auth_choice.html")

    post = get_object_or_404(Post, id=post_id)
    SavedPost.objects.get_or_create(user=request.user, post=post)

    return redirect("post_detail", post_id=post_id)


