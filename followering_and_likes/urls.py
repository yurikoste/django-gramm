from django.urls import path
from . import views

app_name = 'followering_and_likes'

urlpatterns = [
    path('<int:auth_user_id>/<int:user_id>/<int:is_subscribed>', views.follow_unfollow, name='follow_unfollow'),
    path('<int:post_id>/<int:auth_user_id>', views.like_unlike_post, name='like_unlike_post'),
    path('followers', views.get_followers, name='get_followers'),
    path('following', views.get_following, name='get_following'),
    ]
