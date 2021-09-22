from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . models import Following, Likes
from test_app.models import DjangoGrammUser, DjangoGrammPost
from services import counters
from services import checkers


@login_required()
def follow_unfollow(request, auth_user_id, user_id, is_subscribed):
    if request.method == 'POST':
        follower = DjangoGrammUser.objects.get(pk=auth_user_id)
        following = DjangoGrammUser.objects.get(pk=user_id)
        is_subscribed = checkers.is_user_subscribed(request, user_id)
        if not is_subscribed:
            Following.objects.create(user_id=follower, following_user_id=following)
            data = {
                'is_subscribed': True,
                'subscribers_count': counters.get_num_of_followers(user_id)
            }
            return JsonResponse(data, safe=False)
        else:
            Following.objects.filter(user_id=follower, following_user_id=following).delete()
            data = {
                'is_subscribed': False,
                'subscribers_count': counters.get_num_of_followers(user_id)
            }
            return JsonResponse(data, safe=False)


@login_required()
def like_unlike_post(request, post_id, auth_user_id):
    if request.method == 'POST':
        post = DjangoGrammPost.objects.get(pk=post_id)
        user = DjangoGrammUser.objects.get(pk=auth_user_id)
        is_liked = Likes.objects.filter(post=post, user=user).first()
        if is_liked:
            Likes.objects.filter(post=post_id).filter(user=request.user.id).delete()
            data = {
                'is_liked': not is_liked,
                'likes_count': counters.get_num_of_likes(post.id)
            }
            return JsonResponse(data, safe=False)
        else:
            Likes.objects.create(post=post, user=user)
            data = {
                'is_liked': not is_liked,
                'likes_count': counters.get_num_of_likes(post.id)
            }
            return JsonResponse(data, safe=False)


@login_required()
def get_following(request):
    user = DjangoGrammUser.objects.get(pk=request.user.pk)
    return render(request, 'following.html', {"followings": user.following.all})


@login_required()
def get_followers(request):
    user = DjangoGrammUser.objects.get(pk=request.user.pk)
    return render(request, 'followers.html', {"followers": user.followers.all})

