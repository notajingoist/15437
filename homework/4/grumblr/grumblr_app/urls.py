from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'grumblr_app.views.login_register', name='login-register'),
    url(r'^login-register$', 'grumblr_app.views.login_register', name='login-register'),
    
    # url(r'^register-form$', 'grumblr_app.views.register_form', name='register-form'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    # url(r'^reset-form$', 'grumblr_app.views.reset_form', name='reset-form'),
    url(r'^register$', 'grumblr_app.views.register', name='register'),
    url(r'^reset$', 'grumblr_app.views.reset', name='reset'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),


    url(r'^home$', 'grumblr_app.views.home', name='home'),
    url(r'^stream$', 'grumblr_app.views.stream', name='stream'),
    url(r'^profile/(?P<user_id>\d+)$', 'grumblr_app.views.profile', name='profile'),
    url(r'^edit-profile$', 'grumblr_app.views.edit_profile', name='edit-profile'),


    url(r'^search-stream$', 'grumblr_app.views.search_stream', name='search-stream'),
    url(r'^search-home$', 'grumblr_app.views.search_home', name='search-home'),
    url(r'^search-profile/(?P<user_id>\d+)$', 'grumblr_app.views.search_profile', name='search-profile'),
    # url(r'^profile$', 'grumblr_app.views.profile'),
    
    
    url(r'^save-profile-changes$', 'grumblr_app.views.save_profile_changes', name='save-profile-changes'),
    
    # Route for built-in authentication with our own custom login page
    
	 # Route to logout a user and send them back to the login page
    
    
    url(r'^text-post$', 'grumblr_app.views.text_post', name='text-post'),
    url(r'^create-text-post$', 'grumblr_app.views.create_text_post', name='create-text-post'),
    # url(r'^image-post$', 'grumblr_app.views.image_post'),
    # url(r'^video-post$', 'grumblr_app.views.video_post'),
)
