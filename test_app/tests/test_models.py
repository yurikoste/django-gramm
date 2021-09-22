from django.test import TestCase, Client
from ..models import DjangoGrammUser, DjangoGrammPost, Picture
from django.contrib.auth import authenticate
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

    # def test_create_superuser(self):
    #     my_admin = DjangoGrammUser.objects.create_superuser('myemail@test.com', 'aA987654321')
    #     self.assertTrue(my_admin.is_admin)
    #     self.assertTrue(my_admin.is_staff)
    #     self.assertTrue(my_admin.is_active)
    #     self.assertTrue(my_admin.is_superuser)

    def test_DjangoGrammUser_model(self):
        self.post = DjangoGrammUser(
            email='myemail@test.com',
            password='aA987654321',
            first_name='Ivan',
            last_name='Petrov',
            nick_name='IvaP',
            biography='Something very interesting',
        )
        avatar = tempfile.NamedTemporaryFile(suffix=".jpg", dir='test_app/').name
        self.user.avatar = avatar

    def test_DjangoGrammPost_model(self):
        self.post = DjangoGrammPost(description='Test post', tags='#testpost')
        self.post.owner_id = self.user

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        self.client.login(password='aA987654321', email='test@example.com')
        self.assertTrue(self.user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(email='wrong', password='aA987654321')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(email='test@example.com', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


