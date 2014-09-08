from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^hello-world$', 'intro.views.hello_world'),
    url(r'^hello.html$', 'intro.views.hello'),
)
