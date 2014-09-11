from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hw2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'calculator.views.home'),
    url(r'^calculate$', 'calculator.views.calculate'),
    # url(r'^equals$', 'calculator.views.equals'),
    # url(r'^plus$', 'calculator.views.plus'),
    # url(r'^minus$', 'calculator.views.minus'),
    # url(r'^times$', 'calculator.views.times'),
    # url(r'^divide$', 'calculator.views.divide'),
)
