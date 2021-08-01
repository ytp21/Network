from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Following

# Register your models here.
admin.site.register(User, UserAdmin)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('likes',) 

@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    filter_horizontal = ('following',) 


