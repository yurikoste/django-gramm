from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('test_app.urls', namespace='test_app')),
    path('', include('followering_and_likes.urls', namespace='followering_and_likes')),
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
