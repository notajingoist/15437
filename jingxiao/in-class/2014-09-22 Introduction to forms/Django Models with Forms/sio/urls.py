from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'sio.views.home', name='home1'),
    url(r'^home$', 'sio.views.home', name='home2'),
    url(r'^create-student$', 'sio.views.create_student', name='create-student'),
    url(r'^create-course$', 'sio.views.create_course', name='create-course'),
    url(r'^register-student$', 'sio.views.register_student', name='register-student'),
)
