from followering_and_likes.models import Likes
from test_app.models import DjangoGrammUser


def check_is_post_liked_by_logg_user(user, post):
    post_like = Likes.objects.filter(post=post.id)
    for like in post_like:
        if like.user_id == user.id:
            return True
    return False


def is_user_subscribed(request, user_id):
    logged_user = DjangoGrammUser.objects.get(pk=request.user.pk)
    subscribed = logged_user.following.all()
    if not subscribed:
        is_subscribed = 0
    else:
        for subscriber in subscribed:
            if subscriber.following_user_id_id == user_id:
                is_subscribed = 1
                break
            else:
                is_subscribed = 0
    return is_subscribed
