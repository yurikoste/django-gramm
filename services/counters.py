from followering_and_likes.models import Likes, Following


def get_num_of_likes(post_id):
    likes = Likes.objects.filter(post=post_id)
    return likes.count()


def get_num_of_followers(user_id):
    followers = Following.objects.filter(following_user_id=user_id)
    return followers.count()
