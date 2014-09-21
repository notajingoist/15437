from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'grumblr_app.views.home'),
    url(r'^home$', 'grumblr_app.views.home'),
    url(r'^stream$', 'grumblr_app.views.stream'),
    url(r'^profile$', 'grumblr_app.views.profile'),
    url(r'^edit-profile$', 'grumblr_app.views.edit_profile'),
    url(r'^login-register$', 'grumblr_app.views.login_register'),
    url(r'^register$', 'grumblr_app.views.register'),
    url(r'^register-form$', 'grumblr_app.views.register_form'),
    # Route for built-in authentication with our own custom login page
    url(r'^login-form$', 'django.contrib.auth.views.login', {'template_name':'login.html'}),
	 # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^reset-form$', 'grumblr_app.views.reset_form'),
    url(r'^reset$', 'grumblr_app.views.reset'),
    url(r'^text-post$', 'grumblr_app.views.text_post'),
    url(r'^create-text-post$', 'grumblr_app.views.create_text_post'),
    # url(r'^image-post$', 'grumblr_app.views.image_post'),
    # url(r'^video-post$', 'grumblr_app.views.video_post'),
)
