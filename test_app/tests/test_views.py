from django.test import TestCase, Client
from ..models import DjangoGrammUser, DjangoGrammPost
from django.urls import reverse
from ..forms import NewUserForm, LoginForm, UserUpdateForm, DGUserPostForm, DGPictureForm


class ViewsTesting(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create(password='aA987654321', email='test@example.com')
        self.client = Client()

    def test_logout(self):
        self.client.login(password='aA987654321', email='test@example.com')
        self.client.logout()
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_get_index_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    def test_login_page(self):
        resp = self.client.get("/login/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

    def test_register_page(self):
        resp = self.client.get("/register")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'register.html')


class FeedPageTest(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create_user(
            password='aA987654321',
            email='test_feed@example.com',
            username='test_feed@example.com'
        )
        self.client = Client()
        self.client.login(
            password='aA987654321',
            email='test_feed@example.com',
            username='test_feed@example.com',
        )

    def test_feed_page(self):
        resp = self.client.get("/feed")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'feed.html')


class PostPageTest(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create_user(
            password='aA987654321',
            email='test_feed@example.com',
            username='test_feed@example.com',
        )
        self.post = DjangoGrammPost(description='Test post', tags='#testpost')
        self.post.owner_id = self.user

        self.user.save()
        self.post.save()

        self.client = Client()
        self.client.login(password='aA987654321', username='test_feed@example.com')

    def test_post_page(self):
        url = reverse('test_app:show_post', kwargs={'user_post_id': self.post.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'post.html')


class UserPageTest(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create_user(
            password='aA987654321',
            email='test_user_page@example.com',
            username='test_user_page@example.com'
        )
        self.user.save()

        self.client = Client()
        self.client.login(
            password='aA987654321',
            email='test_user_page@example.com',
            username='test_user_page@example.com'
        )

    def test_user_page(self):
        url = reverse('test_app:user_page', kwargs={'user_id': self.user.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'user_page.html')


class EditPostPageTest(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create_user(
            password='aA987654321',
            email='test_edit_post@example.com',
            username='test_edit_post@example.com'
        )
        self.post = DjangoGrammPost(description='Test post', tags='#testpost')
        self.post.owner_id = self.user

        self.user.save()
        self.post.save()

        self.client = Client()
        self.client.login(
            password='aA987654321',
            email='test_edit_post@example.com',
            username='test_edit_post@example.com'
        )

    def test_edit_post_page(self):
        url = reverse('test_app:edit_post', kwargs={'user_post_id': self.post.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'edit_post.html')


class EditUserPageTest(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create_user(
            password='aA987654321',
            email='test_edit_user_page@example.com',
            username='test_edit_user_page@example.com'
        )
        self.user.save()

        self.client = Client()
        self.client.login(
            password='aA987654321',
            email='test_edit_user_page@example.com',
            username='test_edit_user_page@example.com'
        )

    def test_edit_user_page(self):
        resp = self.client.get('/edit_user_page')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'edit_user_page.html')


class AddUserPostTest(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create_user(
            password='aA987654321',
            email='test_add_post@example.com',
            username='test_add_post@example.com'
        )
        self.post = DjangoGrammPost(description='Test post', tags='#testpost')
        self.post.owner_id = self.user

        self.user.save()
        self.post.save()

        self.client = Client()
        self.client.login(
            password='aA987654321',
            email='test_add_post@example.com',
            username='test_add_post@example.com'
        )

    def test_add_post_page(self):
        resp = self.client.get('/add_user_post')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'add_user_post.html')


class PostRequests(TestCase):
    def setUp(self):
        self.user = DjangoGrammUser.objects.create_user(
            password='aA987654321',
            email='test_post_requests@example.com',
            username='test_post_requests@example.com'
        )
        self.unverified_usr = DjangoGrammUser.objects.create_user(
            password='aA987654321',
            email='user_unverified@example.com',
            username='user_unverified@example.com'
        )
        self.user.is_email_verified = True
        self.post = DjangoGrammPost(description='Test post', tags='#testpost')
        self.post.owner_id = self.user

        self.user.save()
        self.unverified_usr.save()
        self.post.save()

        self.client = Client()

    def test_register_request(self):
        data = {'email': 'test_register_requests@example.com', 'password1': 'aA987654321'}
        response = self.client.post('/register', data)
        self.assertEqual(response.status_code, 200)

        form_data = {'password1': 'aA987654321', 'password2': 'aA987654321', 'email': 'test_register_requests@example.com'}
        form = NewUserForm(data=form_data)
        response = self.client.post('/register', form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/',
                             status_code=302, target_status_code=200)

    def test_user_login_request(self):
        data = {'email': 'test_post_requests@example.com', 'password1': 'aA987654321'}
        response = self.client.post('/login/', data)
        self.assertEqual(response.status_code, 302)

        form_data = {'password': 'aA987654321', 'email': 'test_post_requests@example.com'}
        form = LoginForm(data=form_data)
        response = self.client.post('/login/', form_data)
        self.assertEqual(response.status_code, 302)

        form_data = {'password': 'aA987654321', 'email': 'test_register_requests@example.com'}
        form = LoginForm(data=form_data)
        response = self.client.post('/login/', form_data)
        self.assertEqual(response.status_code, 200)

        form_data = {'password': 'aA987654321', 'email': 'user_unverified@example.com'}
        form = LoginForm(data=form_data)
        response = self.client.post('/login/', form_data)
        self.assertEqual(response.status_code, 200)

    def test_add_user_post_request(self):
        # # data = {'email': 'test_post_requests@example.com', 'password1': 'aA987654321'}
        # # response = self.client.post('/test_app/add_user_post/', data)
        # # self.assertEqual(response.status_code, 200)
        # post_data = {'description': 'Test data', 'tags': '#testdata'}
        # img_data = tempfile.NamedTemporaryFile(suffix=".jpg", dir='test_app/').name
        # post_form = DGUserPostForm(data=post_data)
        # page_data = {'description': 'Test data', 'tags': '#testdata', 'img': img_data}
        # img_form = DGPictureForm(data=img_data)
        # response = self.client.post('/test_app/add_user_post', page_data)
        # self.assertEqual(response.status_code, 302)
        pass