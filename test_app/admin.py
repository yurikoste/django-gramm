from django.contrib import admin

# Register your models here.
from . models import DjangoGrammPost, DjangoGrammUser, Picture

admin.site.register(DjangoGrammPost)
admin.site.register(DjangoGrammUser)
admin.site.register(Picture)
