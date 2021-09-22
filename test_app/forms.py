from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import DjangoGrammUser, DjangoGrammPost, Picture


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Please, input your valid email address')

    class Meta:
        model = DjangoGrammUser
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = user.email
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if DjangoGrammUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = DjangoGrammUser
        fields = ['first_name', 'last_name', 'nick_name', 'biography', 'avatar']
        labels = {
            'first_name': "First name",
            'last_name': "Last name",
            'nick_name': "Nickname",
            'biography': "Biography",
            'avatar': 'Avatar'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'nick_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),
            'biography': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Biography'})
        }


class DGUserPostForm(forms.ModelForm):
    class Meta:
        model = DjangoGrammPost
        fields = ['description', 'tags']
        labels = {
            'description': "Post name or description",
            'tags':        "Tags"
        }

        widgets = {
            'description':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post name or description'}),
            'tags':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'})
        }


class DGPictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['img']
        labels = {
            'img': "Select image"
        }

    def __init__(self, *args, **kwargs):
        super(DGPictureForm, self).__init__(*args, **kwargs)
        self.fields['img'].required = False





