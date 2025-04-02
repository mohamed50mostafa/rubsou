from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Post, Comment, Friend, FriendRequest, CommentReaction, PostReaction, Group, GroupRequest

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        profile = Profile(user=user)
        profile.save()
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signin.html', {'error': 'Invalid username or password'})
    return render(request, 'signin.html')

@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def home(request):
    data = {
        'profile': Profile.objects.get(user=request.user),
        'posts': Post.objects.filter(group=None).order_by('-created_at'),
        'my_posts': Post.objects.filter(user=request.user).order_by('-created_at'),
        'my_groups': Group.objects.filter(members=request.user).order_by('-created_at'),
        'groups_i_admin': Group.objects.filter(admin=request.user).order_by('-created_at'),
        'group_requests_sent': GroupRequest.objects.filter(user=request.user).order_by('-created_at'),
        'group_requests_received': GroupRequest.objects.filter(group__admin=request.user).order_by('-created_at'),
        'public_groups': Group.objects.all().order_by('-created_at'),
        'friend_requests_sent': FriendRequest.objects.filter(user=request.user).order_by('-created_at'),
        'friend_requests_received': FriendRequest.objects.filter(friend=request.user).order_by('-created_at'),
        'friends': Friend.objects.filter(user=request.user).order_by('-created_at'),
    }
    return render(request, 'home.html', data)

@login_required(login_url='signin')
def profile(request, username):
    user = User.objects.get(username=username)
    data = {
        'profile': Profile.objects.get(user=user),
    }
    return render(request, 'profile.html', data)

@login_required(login_url='signin')
def edit_profile(request):
    if request.method == 'POST':
        bio = request.POST['bio']
        image = request.FILES['image']
        profile = Profile.objects.get(user=request.user)
        profile.bio = bio
        profile.image = image
        profile.save()
        return redirect('profile', username=request.user.username)
    return render(request, 'edit_profile.html')

@login_required(login_url='signin')
def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    data = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'view_post.html', data)

@login_required(login_url='signin')
def view_group(request, group_id):
    group = Group.objects.get(id=group_id)
    posts = Post.objects.filter(group=group).order_by('-created_at')
    data = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'group.html', data)

@login_required(login_url='signin')
def create_post_group(request, group_id):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        post = Post(user=request.user, group=Group.objects.get(id=group_id), title=title, content=content)
        post.save()
        return redirect('view_group', group_id=group_id)
    return render(request, 'group.html')

@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(user=request.user, title=title, content=content)
        post.save()
        return redirect('view_post', post_id=post.id)
    return render(request, 'home.html')

@login_required(login_url='signin')
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('view_post', post_id=post_id)
    return render(request, 'edit_post.html', {'post': post})

@login_required(login_url='signin')
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('home')

@login_required(login_url='signin')
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST['content']
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(user=request.user, post=post, content=content)
        comment.save()
        return redirect('view_post', post_id=post_id)
    return render(request, 'view_post.html')

@login_required(login_url='signin')
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        content = request.POST['content']
        comment.content = content
        comment.save()
        return redirect('view_post', post_id=comment.post.id)
    return render(request, 'view_post.html', {'comment': comment})

@login_required(login_url='signin')
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('view_post', post_id=comment.post.id)

@login_required(login_url='signin')
def react_post(request, post_id, reaction):
    post = Post.objects.get(id=post_id)
    if PostReaction.objects.filter(user=request.user, post=post).exists():
        return redirect('view_post', post_id=post_id)
    reaction = PostReaction.objects.create(user=request.user, post=post, type=reaction)
    reaction.save()
    return redirect('view_post', post_id=post_id)

@login_required(login_url='signin')
def unreact_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if not PostReaction.objects.filter(user=request.user, post=post).exists():
        return redirect('view_post', post_id=post_id)
    reaction = PostReaction.objects.get(user=request.user, post=post)
    reaction.delete()
    return redirect('view_post', post_id=post_id)

@login_required(login_url='signin')
def react_comment(request, comment_id, reaction):
    comment = Comment.objects.get(id=comment_id)
    if CommentReaction.objects.filter(user=request.user, comment=comment).exists():
        return redirect('view_post', post_id=comment.post.id)
    reaction = CommentReaction.objects.create(user=request.user, comment=comment, type=reaction)
    reaction.save()
    return redirect('view_post', post_id=comment.post.id)

@login_required(login_url='signin')
def unreact_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if not CommentReaction.objects.filter(user=request.user, comment=comment).exists():
        return redirect('view_post', post_id=comment.post.id)
    reaction = CommentReaction.objects.get(user=request.user, comment=comment)
    reaction.delete()
    return redirect('view_post', post_id=comment.post.id)

@login_required(login_url='signin')
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        group = Group(
            admin=request.user,
            name=name,
            description=description,
        )
        group.save()
        group.members.add(request.user)
        group.save()
        return redirect('view_group', group_id=group.id)
    return render(request, 'home.html')

@login_required(login_url='signin')
def join_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.join(request.user)
    group.save()
    return redirect('view_group', group_id=group_id)

@login_required(login_url='signin')
def leave_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.leave(request.user)
    group.save()
    return redirect('home')
@login_required(login_url='signin')
def edit_group(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        group.name = name
        group.description = description
        group.save()
        return redirect('view_group', group_id=group_id)
    return render(request, 'edit_group.html', {'group': group})
@login_required(login_url='signin')
def remove_member(request, group_id, user_id):
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    group.remove_member(user)
    return redirect('view_group', group_id=group_id)
@login_required(login_url='signin')
def send_group_request(request, group_id):
    group = Group.objects.get(id=group_id)
    GroupRequest.objects.create(user=request.user, group=group)
    return redirect('home')

@login_required(login_url='signin')
def accept_group_request(request, group_request_id):
    group_request = GroupRequest.objects.get(id=group_request_id)
    if request.user == group_request.group.admin:
        group_request.accept()
        return redirect('view_group', group_id=group_request.group.id)
    return redirect('home')

@login_required(login_url='signin')
def reject_group_request(request, group_request_id):
    group_request = GroupRequest.objects.get(id=group_request_id)
    if request.user == group_request.group.admin:
        group_request.reject()
    return redirect('home')



@login_required(login_url='signin')
def send_friend_request(request, user_id):
    user = User.objects.get(id=user_id)
    if user == request.user or FriendRequest.objects.filter(user=user, friend=request.user).exists():
        return redirect('home')
    FriendRequest.objects.create(user=request.user, friend=user)
    return redirect('home')

@login_required(login_url='signin')
def accept_friend_request(request, friend_request_id):
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    if request.user == friend_request.friend:
        friend_request.accept()
    return redirect('home')

@login_required(login_url='signin')
def reject_friend_request(request, friend_request_id):
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.reject()
    return redirect('home')

@login_required(login_url='signin')
def unfriend(request, friend_id):
    friend = User.objects.get(id=friend_id)
    user = request.user
    Friend.objects.get(user=user, friend=friend).unfriend()
    Friend.objects.get(user=friend, friend=user).unfriend()
    return redirect('home')




