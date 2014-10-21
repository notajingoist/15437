from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'grumblr_app.views.login_register', name='login-register'),
    url(r'^login-register$', 'grumblr_app.views.login_register', name='login-register'),
    
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^register$', 'grumblr_app.views.register', name='register'),
    url(r'^reset$', 'grumblr_app.views.reset', name='reset'),

    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'grumblr_app.views.confirm_registration', name='confirm'),

    url(r'^home$', 'grumblr_app.views.home', name='home'),
    url(r'^stream$', 'grumblr_app.views.stream', name='stream'),
    url(r'^profile/(?P<user_id>\d+)$', 'grumblr_app.views.profile', name='profile'),
    url(r'^edit-profile$', 'grumblr_app.views.edit_profile', name='edit-profile'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    #url(r'^search/(?P<redirect_name>\w+)/(?P<user_id>\d+)$', 'grumblr_app.views.search', name='search'),
    url(r'^search$', 'grumblr_app.views.search', name='search'),
    # url(r'^search-stream$', 'grumblr_app.views.search_stream', name='search-stream'),
    # url(r'^search-home$', 'grumblr_app.views.search_home', name='search-home'),
    # url(r'^search-profile/(?P<user_id>\d+)$', 'grumblr_app.views.search_profile', name='search-profile'),

    url(r'^text-post$', 'grumblr_app.views.text_post', name='text-post'),

    
    url(r'^comment/(?P<redirect_name>\w+)/(?P<user_id>\d+)/(?P<text_post_id>\d+)$', 'grumblr_app.views.comment', name='comment'),
    url(r'^dislike/(?P<redirect_name>\w+)/(?P<user_id>\d+)/(?P<text_post_id>\d+)$', 'grumblr_app.views.dislike', name='dislike'),

    url(r'^profile-picture/(?P<user_id>\d+)$', 'grumblr_app.views.profile_picture', name='profile-picture'),

    url(r'^follow/(?P<following_id>\d+)$', 'grumblr_app.views.follow', name='follow'),
    url(r'^block/(?P<blocking_id>\d+)$', 'grumblr_app.views.block', name='block'),


    # url(r'^create-text-, 'grumblr_app.views.image_post'),
    # url(r'^video-post$', 'grumblr_app.views.video_post'),post$', 'grumblr_app.views.create_text_post', name='create-text-post'),
    # url(r'^image-post$'
)
