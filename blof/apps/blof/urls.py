from django.conf.urls import patterns, url, include
from rest_framework import routers

from api import views as views


router = routers.DefaultRouter()
router.register(r'users', views.UserView, 'list')
router.register(r'posts', views.PostView, 'list')


urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/$',
        views.AuthView.as_view(),
        name='authenticate')
)