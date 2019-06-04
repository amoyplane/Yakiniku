from django.conf.urls import patterns, url
from . import view

urlpatterns = patterns('',
                       url(r'^$', views.show, name='index'),
                       url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': '/home/anna/Documents/django_py/showImg/static'}),
                       )
