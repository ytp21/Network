import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Following


def index(request):
    page_title = "All Posts"
    everyPost = Post.objects.all()
    posts = everyPost.order_by("-timestamp")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine the range of paginator
    paginator_maxRange = 3
    if paginator.num_pages >= paginator_maxRange:
        if page_obj.number == 1:
            page_range = range(page_obj.number, page_obj.number + paginator_maxRange)
        elif page_obj.number == paginator.num_pages:
            lastPage_range = paginator.num_pages + 1
            page_range = range(lastPage_range - paginator_maxRange, lastPage_range)
        else:
            page_range = range(page_obj.number - 1, page_obj.number + 2)
    elif 0 < paginator.num_pages < paginator_maxRange:
        page_range = range(1, paginator.num_pages + 1)

    return render(request, "network/index.html", {
        "posts": page_obj,
        "page_title": page_title,
        "allPosts_view": True,
        "page_range": page_range,
    })

def following(request):

    page_title = "Following"

    # Must be logged in to view all the following posts
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    try:
        currentUser_following = Following.objects.get(user=request.user.pk)
        followed_user = [following.pk for following in currentUser_following.following.all()]
        everyPost = Post.objects.filter(creator__in=followed_user)
    except Following.DoesNotExist:
        return render(request, "network/index.html", {
            "page_title": page_title,
            "message": "You're not following anyone. Follow people to get started!",
        })

    posts = everyPost.order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine the range of paginator
    paginator_maxRange = 3
    if paginator.num_pages >= paginator_maxRange:
        if page_obj.number == 1:
            page_range = range(page_obj.number, page_obj.number + paginator_maxRange)
        elif page_obj.number == paginator.num_pages:
            lastPage_range = paginator.num_pages + 1
            page_range = range(lastPage_range - paginator_maxRange, lastPage_range)
        else:
            page_range = range(page_obj.number - 1, page_obj.number + 2)
    elif 0 < paginator.num_pages < paginator_maxRange:
        page_range = range(1, paginator.num_pages + 1)

    return render(request, "network/index.html", {
        "posts": page_obj,
        "page_title": page_title,
        "following_view": True,
        "page_range": page_range,
    })

def userProfile(request, name):

    # Obtain data for the requested user profile
    try:
        user_profile = User.objects.get(username=name)
    except User.DoesNotExist:
        return render(request, "network/profile.html", {
            "message": "ERROR: User profile does not exist"
        })

    # Obtain user following
    try:
        user_following = Following.objects.get(user=user_profile.pk)
        following = user_following.following.count()
    except Following.DoesNotExist:
        user_following = []
        following = 0

    # Obtain user followers
    user_follower = Following.objects.filter(following=user_profile.pk)
    followers = user_follower.count()

    # Check if logged in user followed the requested user profile
    try:
        loggedin_user = Following.objects.get(user=request.user)
        loggedin_user_following = loggedin_user.following.all()
    except Following.DoesNotExist:
        loggedin_user_following = []

    # Obtain every posts from requested user 
    posts = Post.objects.filter(creator=user_profile.pk).order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Determine the range of paginator
    paginator_maxRange = 3
    if paginator.num_pages >= paginator_maxRange:
        if page_obj.number == 1:
            page_range = range(page_obj.number, page_obj.number + paginator_maxRange)
        elif page_obj.number == paginator.num_pages:
            lastPage_range = paginator.num_pages + 1
            page_range = range(lastPage_range - paginator_maxRange, lastPage_range)
        else:
            page_range = range(page_obj.number - 1, page_obj.number + 2)
    elif 0 < paginator.num_pages < paginator_maxRange:
        page_range = range(1, paginator.num_pages + 1)

    return render(request, "network/profile.html", {
        "posts": page_obj,
        "user_profile": user_profile,
        "following": following,
        "followers": followers,
        "loggedin_user_following": loggedin_user_following,
        "page_range": page_range,
    })

@csrf_exempt
def createPost(request):

    # Must be logged in to create post
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # Create post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check if post is valid
    data = json.loads(request.body)
    content = data.get("content", "")
    if content == "":
        return JsonResponse({
            "error": "Content is blank"
        }, status=400)

    # Create post 
    Post.objects.create(creator=request.user, content=content)
    return JsonResponse({"message": "Post created successfully."}, status=201)

@csrf_exempt
def updatePost(request, post_id):

    # Get the like status for requested post if the condition is true
    if request.method == "GET":
        post = Post.objects.get(pk=post_id)
        return JsonResponse(post.serialize(), status=201)

    # Update post must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Update like status or edit post content
    data = json.loads(request.body)
    edit_content = data.get("edit_content", "")
    likeButton_triggered = data.get("likeButton_triggered", "")
    if likeButton_triggered:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    if edit_content and request.user == post.creator:
        post.content = edit_content
    post.save()
    return JsonResponse({"message": "Post edited successfully."}, status=201)

@csrf_exempt
def updateUserProfile(request, name):

    # Obtain data for the requested user profile
    try:
        user_profile = User.objects.get(username=name)
    except User.DoesNotExist:
        return render(request, "network/profile.html", {
            "message": "ERROR: User profile does not exist"
        })

    # Get the follow status for requested user profile if the condition is true
    if request.method == "GET":
        try:
            user_following = Following.objects.get(user=request.user)
            return JsonResponse(user_following.serialize(), status=201)
        except Following.DoesNotExist:
            return JsonResponse({"error": "You are not following anyone"})

    # Update following status in the server
    if request.method == "PUT":
        data = json.loads(request.body)
        followButton_triggered = data.get("followButton_triggered", "")
        if request.user.is_authenticated and followButton_triggered:
            try:
                current_user = Following.objects.get(user=request.user)
                if user_profile in current_user.following.all():
                    current_user.following.remove(user_profile.pk)
                else:
                    current_user.following.add(user_profile.pk)
                current_user.save()
                return HttpResponse(status=204)
            except Following.DoesNotExist:
                new = Following(user=request.user)
                new.save()
                new.following.add(user_profile)
        else:
            return HttpResponseRedirect(reverse('login'))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
