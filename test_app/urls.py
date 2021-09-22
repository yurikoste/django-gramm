from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'test_app'

urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register_request, name="register"),
    url(r'^login/$', views.user_login, name='login'),
    url('logout', views.user_logout, name='logout'),
    path('user_page/<int:user_id>', views.display_user_page, name='user_page'),
    path('edit_user_page', views.edit_user_page, name='edit_user_page'),
    path('activate_user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('add_user_post', views.add_user_post, name='add_user_post'),
    path('show_post/<int:user_post_id>', views.show_post, name='show_post'),
    path('edit_post/<int:user_post_id>', views.edit_post, name='edit_post'),
    path('feed', views.show_feed, name='show_feed')
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)