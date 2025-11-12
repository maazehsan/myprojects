from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Post,Like,Follow

POSTS_PER_PAGE = 2

def index(request):
    posts = Post.objects.select_related("author").annotate(num_likes=Count("likes")).order_by("-created_at")
    page = Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get("page"))
    return render(request, "network/index.html", {
        "page_obj": page})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index3"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index3"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index3"))
    else:
        return render(request, "network/register.html")

# profile page

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by("-created_at")
    page = Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get("page"))
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    is_following = request.user.is_authenticated and Follow.objects.filter(
        follower=request.user, following=profile_user
    ).exists()
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })

@login_required
def following(request):
    following_ids = request.user.following.values_list("following_id", flat=True)
    posts = Post.objects.filter(author_id__in=following_ids).order_by("-created_at")
    page = Paginator(posts, POSTS_PER_PAGE).get_page(request.GET.get("page"))
    return render(request, "network/index.html", {"page_obj": page})

@require_http_methods(["GET", "POST"])
def posts_api(request):
    # for get
    if request.method == "GET":
        page_num = request.GET.get("page", 1)
        posts = Post.objects.select_related("author").order_by("-created_at")
        page = Paginator(posts, POSTS_PER_PAGE).get_page(page_num)
        data = [p.serialize(me=request.user if request.user.is_authenticated else None) for p in page]
        return JsonResponse({
            "results": data,
            "page": page.number,
            "num_pages": page.paginator.num_pages,
            "has_next": page.has_next(),
            "has_previous": page.has_previous(),
        })

    # for post
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Login required")
    content = (request.POST.get("content") or "").strip() if request.POST else ""
    if not content:
        return HttpResponseBadRequest("Content required")
    post = Post.objects.create(author=request.user, content=content)
    return JsonResponse(post.serialize(me=request.user), status=201)

@require_http_methods(["GET", "PUT"])
def post_detail_api(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "GET":
        return JsonResponse(post.serialize(me=request.user if request.user.is_authenticated else None))

    if not request.user.is_authenticated or request.user != post.author:
        return HttpResponseForbidden("Not allowed")

    data = json.loads(request.body.decode("utf-8"))
    new_content = (data.get("content") or "").strip()
    if not new_content:
        return HttpResponseBadRequest("Content required")
    post.content = new_content
    post.save()
    return JsonResponse(post.serialize(me=request.user))
#like / unlike
@login_required
@require_http_methods(["POST"])
def like_toggle_api(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({"liked": liked, "likes": post.likes.count()})
# follow / unfollow
@login_required
@require_http_methods(["POST"])
def follow_toggle_api(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return HttpResponseBadRequest("Cannot follow yourself")
    rel, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        rel.delete()
        following = False
    else:
        following = True
    return JsonResponse({
        "following": following,
        "followers_count": target.followers.count(),
        "following_count": target.following.count(),
    })
