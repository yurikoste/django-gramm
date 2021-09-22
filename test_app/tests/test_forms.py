from django.test import TestCase
from .. models import DjangoGrammUser
from .. forms import NewUserForm, LoginForm, UserUpdateForm


class TestForms(TestCase):
    def test_new_user_form(self):
        form_data = {'password1': 'aA987654321', 'password2': 'aA987654321', 'email': 'test_add_post@example.com'}
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        result = form.save()
        user = DjangoGrammUser(password='aA987654321', email='test_add_post@example.com')
        self.assertEqual(result.email, user.email)

    def test_login_form_correct(self):
        form_data = {'password': 'aA987654321', 'email': 'test_add_post@example.com'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {'password': None, 'email': 'test_add_post@example.com'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_update_form_valid(self):
        form_data = {
            'first_name': 'Ann',
            'last_name': 'Karenina',
            'nickname': 'AKa',
            'biography': 'Notorious by dying due to train'
        }
        form = UserUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())