from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="post_liked", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "likes": [user.username for user in self.likes.all()],
        }
    
class Following(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
    following = models.ManyToManyField("User", related_name="following")

    def serialize(self):
        return {
            "user": self.user.username,
            "following": [following.username for following in self.following.all()],
        }