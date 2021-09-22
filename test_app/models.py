from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


class DjangoGrammUser(AbstractUser):
    email               = models.EmailField(max_length=200, verbose_name='email')
    password            = models.CharField(max_length=200)
    first_name          = models.CharField(max_length=80, blank=True, null=True)
    last_name           = models.CharField(max_length=80, blank=True, null=True)
    nick_name           = models.CharField(max_length=80, blank=True, null=True)
    biography           = models.CharField(max_length=500, blank=True, null=True)
    avatar              = models.ImageField(upload_to='img/avatars', blank=True, null=True)
    reg_date            = models.DateTimeField(auto_now_add=True)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_email_verified   = models.BooleanField(default=False)


class DjangoGrammPost(models.Model):
    owner_id = models.ForeignKey(DjangoGrammUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    tags = models.CharField(max_length=300, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']


class Picture(models.Model):
    post_id = models.ForeignKey(DjangoGrammPost, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img/imgs')

