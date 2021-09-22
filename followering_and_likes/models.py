from django.db import models
from test_app.models import DjangoGrammUser, DjangoGrammPost


class Following(models.Model):
    user_id = models.ForeignKey(DjangoGrammUser, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(DjangoGrammUser, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'following_user_id'], name="unique_followers")
        ]

        ordering = ["-created"]


class Likes(models.Model):
    post = models.ForeignKey(DjangoGrammPost, related_name='liked_posts', on_delete=models.CASCADE)
    user = models.ForeignKey(DjangoGrammUser, related_name='user_liked', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
