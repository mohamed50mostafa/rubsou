from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),
    
    # Authentication routes
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    
    # Profile routes
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # Home route
    path('', views.home, name='home'),

    # Group routes
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.view_group, name='view_group'),
    path('edit_group/<int:group_id>/', views.edit_group, name='edit_group'),
    path('send_group_request/<int:group_id>/', views.send_group_request, name='send_group_request'),
    path('accept_group_request/<int:group_request_id>/', views.accept_group_request, name='accept_group_request'),
    path('reject_group_request/<int:group_request_id>/', views.reject_group_request, name='reject_group_request'),
    path('join_group/<int:group_id>/', views.join_group, name='join_group'),
    path('leave_group/<int:group_id>/', views.leave_group, name='leave_group'),
    path('remove_member/<int:group_id>/<int:user_id>/', views.remove_member, name='remove_member'),

    # Post routes
    path('create_post/', views.create_post, name='create_post'),
    path('create_post/<int:group_id>/', views.create_post_group, name='create_post_group'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('view_post/<int:post_id>/', views.view_post, name='view_post'),
    path('react_post/<int:post_id>/<str:reaction>/', views.react_post, name='react_post'),
    path('unreact_post/<int:post_id>/', views.unreact_post, name='unreact_post'),

    # Comment routes
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('react_comment/<int:comment_id>/<str:reaction>/', views.react_comment, name='react_comment'),
    path('unreact_comment/<int:comment_id>/', views.unreact_comment, name='unreact_comment'),

    # Friend request routes
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('unfriend/<int:friend_id>/', views.unfriend, name='unfriend'),
    path('accept_friend_request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:friend_request_id>/', views.reject_friend_request, name='reject_friend_request'),
]


