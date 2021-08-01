
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("user_profile/<str:name>", views.userProfile, name="userProfile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("create_post", views.createPost, name="createPost"),
    path("update_post/<int:post_id>", views.updatePost, name="updatePost"),
    path("update_userProfile/<str:name>", views.updateUserProfile, name="updateUserProfile"),
]
