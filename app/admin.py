from django.contrib import admin
from .models import Profile, Post, Comment, CommentReaction, PostReaction, Group, GroupRequest, Friend, FriendRequest
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentReaction)
admin.site.register(PostReaction)
admin.site.register(Group)
admin.site.register(GroupRequest)
admin.site.register(Friend)
admin.site.register(FriendRequest)
