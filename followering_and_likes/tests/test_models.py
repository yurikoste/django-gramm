from django.test import TestCase, Client
from test_app.models import DjangoGrammUser, DjangoGrammPost, Picture
from followering_and_likes.models import Following, Likes
import tempfile


class ModelsTests(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create(password='aA987654321', email='test@example.com')
        avatar = tempfile.NamedTemporaryFile(suffix=".jpg", dir='test_app/').name
        self.user.avatar = avatar

        self.post = DjangoGrammPost(description='Test post', tags='#testpost')
        self.post.owner_id = self.user

        pic = tempfile.NamedTemporaryFile(suffix=".jpg", dir='test_app/').name
        self.image = Picture(img=pic, post_id=self.post)
        self.client = Client()

    def create_second_user(self):
        self.user2 = DjangoGrammUser.objects.create(
            password='aA987654321',
            email='test2@example.com',
            username='test2@example.com'
        )

    def test_following(self):
        user2 = DjangoGrammUser.objects.create(
            password='aA987654321',
            email='test2@example.com',
            username='test2@example.com'
        )
        self.follow = Following.objects.create(user_id=self.user, following_user_id=user2)
        self.assertTrue(self.user.followers is not None)
        self.assertEqual(self.user.following.first(), user2.followers.first())

    def test_likes(self):
        user2 = DjangoGrammUser.objects.create(
            password='aA987654321',
            email='test2@example.com',
            username='test2@example.com'
        )
        self.post = DjangoGrammPost(description='Test post', tags='#testpost')
        self.post.owner_id = self.user
        self.post.save()
        liked_post = Likes.objects.create(post=self.post, user=user2)
        self.assertEqual(liked_post.user, user2)
