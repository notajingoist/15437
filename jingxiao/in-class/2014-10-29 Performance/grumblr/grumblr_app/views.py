from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.core import serializers
from mimetypes import guess_type
from django.utils import timezone
from datetime import datetime

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail

from models import *
from forms import *

import sys
from django.http import JsonResponse
import json
# Create your views here.

def get_default_context(request):
    context = {}
    context['dislikes'] = request.user.dislikes.all()
    context['comment_redirect'] = request.resolver_match.url_name
    context['dislike_redirect'] = request.resolver_match.url_name

    initial_data = { 'redirect_name': request.resolver_match.url_name }
    context['search_form'] = SearchForm(initial=initial_data)

    return context

@login_required
def redirect_home(request, errors):
    context = {}
    context['errors'] = errors
    context['dislikes'] = request.user.dislikes.all()
    context['comment_redirect'] = 'home'
    context['dislike_redirect'] = 'home'

    initial_data = { 'redirect_name': 'home', 'result_type': 'home' }
    context['search_form'] = SearchForm(initial=initial_data)
    context['text_posts'] = TextPost.get_posts_from_user(request.user)
    return render(request, 'home.html', context)

# home
@login_required
def home(request):
    context = {}
    context['dislikes'] = request.user.dislikes.all()
    context['comment_redirect'] = 'home'
    context['dislike_redirect'] = 'home'

    initial_data = { 'redirect_name': 'home', 'result_type': 'home' }
    context['search_form'] = SearchForm(initial=initial_data)
    context['text_posts'] = TextPost.get_posts_from_user(request.user)

    comment_forms = {}
    context['comment_forms'] = comment_forms

    for post in context['text_posts']:
        comment_form = CommentForm()
        comment_forms[post.id] = comment_form

    return render(request, 'home.html', context)

# stream
@login_required
def stream(request):
    context = {}
    context['dislikes'] = request.user.dislikes.all()
    context['comment_redirect'] = 'stream'
    context['dislike_redirect'] = 'stream'

    initial_data = { 'redirect_name': 'stream', 'result_type': 'stream' }
    context['search_form'] = SearchForm(initial=initial_data)
    context['text_posts'] = TextPost.get_stream_posts(request.user)

    comment_forms = {}
    context['comment_forms'] = comment_forms

    for post in context['text_posts']:
        comment_form = CommentForm()
        comment_forms[post.id] = comment_form

    return render(request, 'stream.html', context)

@login_required
@transaction.atomic
def settings(request):
    context = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # errors = []
    # context['errors'] = errors
    context['user'] = request.user
    context['user_profile'] = user_profile
    context['picture-src'] = ''

    initial_data = { 'redirect_name': 'stream', 'result_type': 'stream' }
    context['search_form'] = SearchForm(initial=initial_data)
    if request.method == 'GET':
        context['form'] = SetPasswordForm()
        return render(request, 'settings.html', context)

    form = SetPasswordForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        context['non_field_errors'] = form.non_field_errors()
        return render(request, 'settings.html', context)

    if not request.user.check_password(form.cleaned_data['password']):
        context['incorrect_password'] = "Incorrect password."
        return render(request, 'settings.html', context)
    form.save(username=request.user.username)
    update_session_auth_hash(request, request.user)

    return render(request, 'home.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    context['user'] = user
    context['user_profile'] = user_profile
    context['picture-src'] = ''

    initial_data = { 'redirect_name': 'stream', 'result_type': 'stream' }
    context['search_form'] = SearchForm(initial=initial_data)

    initial_user = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'email': user.email,
                    'location': user_profile.location,
                    'about': user_profile.about,
                    'picture': user_profile.picture
                }

    if request.method == 'GET':
        context['form'] = UserProfileForm(initial=initial_user)
        return render(request, 'edit-profile.html', context)

    form = UserProfileForm(request.POST, request.FILES, initial=initial_user)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'edit-profile.html', context)

    form.save(user_instance=request.user, user_profile_instance=user_profile)
    update_session_auth_hash(request, user)

    return render(request, 'edit-profile.html', context)

@login_required
@transaction.atomic
def text_post(request):
    context = {}
    initial_data = { 'redirect_name': 'stream', 'result_type': 'stream' }
    context['search_form'] = SearchForm(initial=initial_data)

    if request.method == 'GET':
        context['form'] = TextPostForm()
        return render(request, 'text-post.html', context)

    new_text_post = TextPost(user=request.user)
    form = TextPostForm(request.POST, instance=new_text_post)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'text-post.html', context)

    form.save()
    return redirect(reverse('home'))

@login_required
@transaction.atomic
def image_post(request):
    context = {}
    initial_data = { 'redirect_name': 'stream', 'result_type': 'stream' }
    context['search_form'] = SearchForm(initial=initial_data)

    if request.method == 'GET':
        context['form'] = ImagePostForm()
        return render(request, 'image-post.html', context)

    new_image_post = TextPost(user=request.user)
    form = ImagePostForm(request.POST, request.FILES, instance=new_image_post)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'image-post.html', context)

    form.save();
    return redirect(reverse('home'))


@login_required
def get_user(request):
    if request.method == 'GET':
        if request.is_ajax():
            if 'user_id' in request.GET and request.GET['user_id']:
                
                user = User.objects.get(id=request.GET['user_id'])
                data = serializers.serialize('json', [user])
                return HttpResponse(data, content_type='application/json')

    data = serializers.serialize('json', User.objects.none())
    return HttpResponse(data, content_type='application/json')

@login_required
def fetch_comments(request):
    if request.method == 'GET':
        if request.is_ajax():
            if 'post_id' in request.GET and request.GET['post_id']:
                
                text_post = TextPost.objects.get(id=request.GET['post_id'])
                comments = text_post.comments.all()
                data = serializers.serialize('json', comments)
                return HttpResponse(data, content_type='application/json')

    data = serializers.serialize('json', Comment.objects.none())
    return HttpResponse(data, content_type='application/json')

@login_required
def fetch_posts(request):
    if request.method == 'GET':
        if request.is_ajax():
            if 'current_path' in request.GET and request.GET['current_path']:

                if 'last_update' in request.GET and request.GET['last_update']:
                    # text_posts = TextPost.objects.exclude(date_created__lt=datetime.date(last_udpate))
                    # print >>sys.stderr, datetime.datetime.now()
                    pass
                else:
                    pass

    data = serializers.serialize('json', TextPost.objects.none())
    return HttpResponse(data, content_type='application/json')

@login_required
@transaction.atomic
def comment(request, redirect_name, user_id, text_post_id):
    context = {}

    initial_data = { 'redirect_name': 'stream', 'result_type': 'stream' }
    context['search_form'] = SearchForm(initial=initial_data)
    user = User.objects.filter(id=user_id)

    context['comment_redirect'] = redirect_name
    context['user_id'] = user_id
    text_post = TextPost.objects.get(id=text_post_id)
    context['text_post'] = text_post

    if request.method == 'GET':
        data = serializers.serialize('json', text_post.comments.all())
        return HttpResponse(data, content_type='application/json')

    new_comment = Comment(user=request.user, post=text_post)
    form = CommentForm(request.POST, instance=new_comment)
    context['form'] = form

    if not form.is_valid():
        errors = json.dumps([{'errors': True}, form.errors])
        return HttpResponse(errors, content_type='application/json')

    form.save()

    data = serializers.serialize('json', [new_comment])
    return HttpResponse(data, content_type='application/json')

@login_required
def search_profile(request, user_id):
    context = {}
    errors = []
    context['errors'] = errors

    if request.method == 'GET':
        return redirect(reverse('profile', kwargs={'user_id':user_id}))

    search_form = SearchForm(request.POST)
    context['search_form'] = search_form

    if not search_form.is_valid():
        raise Http404

    redirect_name = search_form.cleaned_data['redirect_name']
    context['comment_redirect'] = redirect_name
    context['dislike_redirect'] = redirect_name
    
    user_id = user_id
    if len(User.objects.filter(id=user_id)) <= 0:
        errors.append('User does not exist.')
    if errors:
        raise Http404

    user = User.objects.filter(id=user_id)[0]
    text_posts = TextPost.objects.filter(user=user_id)
    context['text_posts_count'] = len(text_posts)
    context['text_posts'] = text_posts.order_by('-date_created')
    context['user'] = user
    user_profile = UserProfile.objects.get(user=user)
    context['user_profile'] = user_profile

    comment_forms = {}
    context['comment_forms'] = comment_forms

    for post in context['text_posts']:
        comment_form = CommentForm()
        comment_forms[post.id] = comment_form

    if len(user.email) > 16:
        new_end_index = 13
        context['email_curtailed'] = user.email[:new_end_index]
    else:
        text_posts = TextPost.get_stream_posts(user=request.user)

    context['keyword'] = search_form.cleaned_data['keyword']
    text_posts = text_posts.filter(text__icontains=context['keyword'])
    if len(text_posts) <= 0:
        errors.append('No search results found for ' + context['keyword'])
    context['text_posts'] = text_posts.order_by('-date_created')

    return render(request, redirect_name + '.html', context)

@login_required
def search(request):
    context = {}
    errors = []
    context['errors'] = errors
    context['user'] = request.user

    if request.method == 'GET':
        raise Http404

    search_form = SearchForm(request.POST)
    context['search_form'] = search_form
    

    if not search_form.is_valid():
        raise Http404

    redirect_name = search_form.cleaned_data['redirect_name']
    result_type = search_form.cleaned_data['result_type']
    context['comment_redirect'] = redirect_name
    context['dislike_redirect'] = redirect_name
    

    if result_type == 'home':
        text_posts = TextPost.objects.filter(user=request.user)
    elif result_type =='stream':
        text_posts = TextPost.get_stream_posts(user=request.user)
    else:
        home_posts = TextPost.objects.filter(user=request.user)
        stream_posts = TextPost.get_stream_posts(user=request.user)
        text_posts = home_posts | stream_posts


    context['keyword'] = search_form.cleaned_data['keyword']
    text_posts = text_posts.filter(text__icontains=context['keyword'])
    if len(text_posts) <= 0:
        errors.append('No search results found for ' + context['keyword'])
    context['text_posts'] = text_posts.order_by('-date_created')

    comment_forms = {}
    context['comment_forms'] = comment_forms
    for post in context['text_posts']:
        comment_form = CommentForm()
        comment_forms[post.id] = comment_form

    return render(request, redirect_name + '.html', context)

@login_required
def follow(request, following_id):
    followed_user = User.objects.get(id=following_id)
    if (request.user != followed_user): 
        user_profile = UserProfile.objects.get(user=request.user)
        followed_profile = UserProfile.objects.get(id=following_id)
        user_profile.follows.add(followed_profile)
        username = followed_user.username
    return redirect(reverse('profile', kwargs={'username':username}))

@login_required
def block(request, blocking_id):
    blocked_user = User.objects.get(id=blocking_id)
    if (request.user != blocked_user): 
        user_profile = UserProfile.objects.get(user=request.user)
        blocked_profile = UserProfile.objects.get(id=blocking_id)
        user_profile.blocks.add(blocked_profile)
        username = blocked_user.username
    return redirect(reverse('profile', kwargs={'username':username}))

@login_required
def profile(request, username):
    context = {}
    errors = []
    context['errors'] = errors
    context['dislike_redirect'] = 'profile'
    context['comment_redirect'] = 'profile'
    user = User.objects.filter(username__exact=username)
    if len(user) <= 0:
        errors.append('User does not exist.')

    if errors:
        text_posts = TextPost.objects.filter(user=request.user)
        context['text_posts'] = TextPost.objects.filter(user=request.user).order_by('-date_created')
        return redirect_home(request, errors)

    user = user[0]
    user_id = user.id

    initial_data = {
                    'redirect_name': 'profile',
                    'user_id': user_id
                }
    context['search_form'] = SearchForm(initial=initial_data)

    text_posts = TextPost.objects.filter(user=user_id)
    context['text_posts'] = text_posts.order_by('-date_created')
    context['text_posts_count'] = len(text_posts)
    context['user'] = user
    context['user_fn_len'] = len(user.first_name)
    context['user_ln_len'] = len(user.last_name)

    comment_forms = {}
    context['comment_forms'] = comment_forms

    for post in context['text_posts']:
        comment_form = CommentForm()
        comment_forms[post.id] = comment_form


    user_profile = UserProfile.objects.get(user=user)
    context['user_profile'] = user_profile

    if len(user.email) > 16:
        new_end_index = 13
        context['email_curtailed'] = user.email[:new_end_index]

    return render(request, 'profile.html', context)

@login_required
def profile_picture(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    if not user_profile:
        raise Http404

    content_type = guess_type(user_profile.picture.name)
    return HttpResponse(user_profile.picture, content_type=content_type)


@login_required
def image(request, post_id):
    text_post = get_object_or_404(TextPost, id=post_id)
    if not text_post:
        raise Http404

    content_type = guess_type(text_post.image.name)
    return HttpResponse(text_post.image, content_type=content_type)

@login_required
def dislike(request, redirect_name, user_id, text_post_id):
    context = {}
    dislikes = Dislike.objects.all()
    context['dislike_redirect'] = redirect_name

    text_post = TextPost.objects.get(id=text_post_id)

    exists = False
    for dislike in dislikes:
        if (dislike.user == request.user and dislike.post == text_post):
            exists = True

    if not exists:
        dislike = Dislike(user=request.user, post=text_post)
        dislike.save()

    context['dislikes'] = dislikes

    username = User.objects.get(id=user_id).username    

    if (redirect_name == 'profile'):
        return redirect(reverse('profile', kwargs={'username':username}))
    else:
       return redirect(reverse(redirect_name))
    
@login_required
@transaction.atomic
def stream_dislike(request, user_id, text_post_id):
    context = dislike_post(request, user_id, text_post_id)
    context['user'] = request.user
    context['text_posts'] = TextPost.get_posts_without_user(request.user)
    return render(request, 'stream.html', context)


def login_register(request):
    context = {}

    #if request.method == 'GET':
    return render(request, 'login-register.html', context)

@transaction.atomic
def confirm_reset(request, username, token):
    context = {}
    context['username'] = username
    context['token'] = token
    context['reset_message'] = 'Reset your password.'
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    if request.method == 'GET':
        form = ResetPasswordForm()
        context['form'] = form
        return render(request, 'confirm-reset.html', context)

    form = ResetPasswordForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        raise Http404

    form.save(username)

    context['confirmed'] = 'Your password has been reset.'

    return render(request, 'login-register.html', context)

def reset(request):
    context = {}
    errors = []
    context['errors'] = errors

    if request.method == 'GET':
        context['form'] = ResetForm()
        return render(request, 'reset.html', context)


    form = ResetForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'reset.html', context)

    user = User.objects.get(email=form.cleaned_data['email'])
    token = default_token_generator.make_token(user)

    email_body = """
    Please click the link below to reset your password:

    http://%s%s
    """ % (request.get_host(),
            reverse('confirm-reset', args=(user.username, token)))

    send_mail(subject="Reset Your Password",
                message=email_body,
                from_email="jing+xiao@andrew.cmu.edu",
                recipient_list=[user.email])
    
    context['email'] = form.cleaned_data['email']

    context['reset_message'] = 'You have been sent an email with a link to reset your password.'

    return render(request, 'reset.html', context)


def register_form(request):
    context = {}
    return render(request, 'register.html', context) 

@transaction.atomic
def register(request):
    context = {}
    errors = []
    context['errors'] = errors

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)


    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'register.html', context)

    # Creates the new user from the valid form data
    new_user = form.save()

    token = default_token_generator.make_token(new_user)

    email_body = """
    Welcome to Grumblr! Please click the link below to verify your email 
    address and complete the registration of your account:

    http://%s%s
    """ % (request.get_host(),
            reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
                message=email_body,
                from_email="jing+xiao@andrew.cmu.edu",
                recipient_list=[new_user.email])
    context['email'] = form.cleaned_data['email']


    return render(request, 'needs-confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active = True
    user.save()

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.save()

    return render(request, 'confirmed.html', {})

