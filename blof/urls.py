from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='blof.html'), name='home'),
    url(r'', include('blof.apps.blof.urls'))
)
