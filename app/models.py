from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Group(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groups_moderated')
    members = models.ManyToManyField(User, related_name='groups_joined')
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    def join(self, user):
        if user in self.members.all():
            return False
        if user == self.admin:
            return False
        self.members.add(user)
        self.save()
        return True
    def leave(self, user):
        if user in self.members.all():
            self.members.remove(user)
            self.save()
            return True
        return False
    def remove_member(self, user):
        if user in self.members.all():
            self.members.remove(user)
            self.save()
            return True
        return False


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts', default=None, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title} at {self.created_at}"


class PostReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_reactions')
    type = models.CharField(max_length=100, choices=[('like', 'like'), ('love', 'love'), ('haha', 'haha'), ('sad', 'sad'), ('wow', 'wow'), ('angry', 'angry')] , default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username} reacted to {self.post.title} at {self.created_at}"

class CommentReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reactions')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reactions')
    type = models.CharField(max_length=100, choices=[('like', 'like'), ('love', 'love'), ('haha', 'haha'), ('sad', 'sad'), ('wow', 'wow'), ('angry', 'angry')] , default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username} reacted to {self.comment.content} at {self.created_at}"

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} and {self.friend.username}"
    def unfriend(self):
        self.delete()
        return True

class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} sent a friend request to {self.friend.username}"
    def accept(self):
        if self.user in self.friend.friends.all():
            return False
        Friend.objects.create(user=self.user, friend=self.friend)
        Friend.objects.create(user=self.friend, friend=self.user)
        self.delete()
        return True
    def reject(self):
        self.delete()
        return True

class GroupRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_requests')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_requests_sent')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} sent a group request to {self.group.name}"
    def accept(self):
        if self.user in self.group.members.all():
            return False
        self.group.members.add(self.user)
        self.delete()
        return True
    def reject(self):
        self.delete()
        return True

