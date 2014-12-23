from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'courseproj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'courseapp.views.home'),
    url(r'^create-student$', 'courseapp.views.create_student'),
    url(r'^create-course$', 'courseapp.views.create_course'),
    url(r'^register-for-course$', 'courseapp.views.register_for_course'),
)
