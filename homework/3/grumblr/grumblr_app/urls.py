from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'grumblr_app.views.login_register'),
    url(r'^home$', 'grumblr_app.views.home'),
    url(r'^stream$', 'grumblr_app.views.stream'),
    url(r'^profile$', 'grumblr_app.views.profile'),
    url(r'^edit-profile$', 'grumblr_app.views.edit_profile'),
    url(r'^login-register$', 'grumblr_app.views.login_register'),
    url(r'^text-post$', 'grumblr_app.views.text_post'),
    url(r'^image-post$', 'grumblr_app.views.image_post'),
    url(r'^video-post$', 'grumblr_app.views.video_post'),
)
