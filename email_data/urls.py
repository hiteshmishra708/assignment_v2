from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.views.static import serve
from django.conf import settings
 
router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^connect/$', views.connect, name='connect'),
    url(r'^extract/$', views.extract, name='extract-data'),
    url(r'^download/(?P<file>[\w\-\.*]+)', views.download, name='download'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^$', views.index, name='index'),
]