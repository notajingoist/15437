from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from mimetypes import guess_type

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

# Create your views here.

def get_default_context(request):
    context = {}
    context['dislikes'] = request.user.dislikes.all()
    context['comment_redirect'] = request.resolver_match.url_name
    context['dislike_redirect'] = request.resolver_match.url_name

    initial_data = { 'redirect_name': request.resolver_match.url_name }
    context['search_form'] = SearchForm(initial=initial_data)

    return context

# home
@login_required
def home(request):
    context = {}
    context['dislikes'] = request.user.dislikes.all()
    context['comment_redirect'] = 'home'
    context['dislike_redirect'] = 'home'

    initial_data = { 'redirect_name': 'home' }
    context['search_form'] = SearchForm(initial=initial_data)
    context['text_posts'] = TextPost.get_posts_from_user(request.user)
    return render(request, 'home.html', context)

# stream
@login_required
def stream(request):
    context = {}
    context['dislikes'] = request.user.dislikes.all()
    context['comment_redirect'] = 'stream'
    context['dislike_redirect'] = 'stream'

    initial_data = { 'redirect_name': 'stream' }
    context['search_form'] = SearchForm(initial=initial_data)
    context['text_posts'] = TextPost.get_stream_posts(request.user)
    return render(request, 'stream.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # errors = []
    # context['errors'] = errors
    context['user'] = user
    context['user_profile'] = user_profile
    context['picture-src'] = ''

    initial_data = { 'redirect_name': 'stream' }
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
    initial_data = { 'redirect_name': 'stream' }
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
def comment(request, redirect_name, user_id, text_post_id):
    context = {}
    initial_data = { 'redirect_name': 'stream' }
    context['search_form'] = SearchForm(initial=initial_data)

    context['comment_redirect'] = redirect_name
    context['user_id'] = user_id
    text_post = TextPost.objects.get(id=text_post_id)
    context['text_post'] = text_post

    if request.method == 'GET':
        context['form'] = CommentForm()
        return render(request, 'comment.html', context)

    new_comment = Comment(user=request.user, post=text_post)
    form = CommentForm(request.POST, instance=new_comment)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'comment.html', context)

    form.save()

    if (redirect_name == 'profile'):
        return redirect(reverse('profile', kwargs={'user_id':user_id}))
    else:
       return redirect(reverse(redirect_name))

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
    #redirect_name = search_form.data['redirect_name']

    if not search_form.is_valid():
        raise Http404

    redirect_name = search_form.cleaned_data['redirect_name']
    context['comment_redirect'] = redirect_name
    context['dislike_redirect'] = redirect_name
    

    if redirect_name == 'home':
        text_posts = TextPost.objects.filter(user=request.user)

    elif redirect_name == 'profile':
        #print >>sys.stderr, search_form.data['user_id']
        user_id = search_form.data['user_id']
        if len(User.objects.filter(id=user_id)) <= 0:
            errors.append('User does not exist.')
        if errors:
            #return redirect(reverse(redirect_name))
            text_posts = TextPost.objects.filter(user=request.user)
            context['text_posts'] = TextPost.objects.filter(user=request.user).order_by('-date_created')
            return render(request, 'home.html', context)

        user = User.objects.filter(id=user_id)[0]
        text_posts = TextPost.objects.filter(user=user_id)
        context['text_posts_count'] = len(text_posts)
        context['text_posts'] = text_posts.order_by('-date_created')
        context['user'] = user
        user_profile = UserProfile.objects.get(user=user)
        context['user_profile'] = user_profile

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

    #print >>sys.stderr, search_form.data['redirect_name']
    return render(request, redirect_name + '.html', context)

@login_required
def follow(request, following_id):
    followed_user = User.objects.get(id=following_id)
    if (request.user != followed_user): 
        user_profile = UserProfile.objects.get(user=request.user)
        followed_profile = UserProfile.objects.get(id=following_id)
        user_profile.follows.add(followed_profile)
    return redirect(reverse('profile', kwargs={'user_id':following_id}))

@login_required
def block(request, blocking_id):
    blocked_user = User.objects.get(id=blocking_id)
    if (request.user != blocked_user): 
        user_profile = UserProfile.objects.get(user=request.user)
        blocked_profile = UserProfile.objects.get(id=blocking_id)
        user_profile.blocks.add(blocked_profile)
    return redirect(reverse('profile', kwargs={'user_id':blocking_id}))

@login_required
def profile(request, user_id):
    context = {}
    errors = []
    context['errors'] = errors
    context['dislike_redirect'] = 'profile'
    context['comment_redirect'] = 'profile'
    initial_data = {
                    'redirect_name': 'profile',
                    'user_id': user_id
                }
    context['search_form'] = SearchForm(initial=initial_data)

    if len(User.objects.filter(id=user_id)) <= 0:
        errors.append('User does not exist.')

    if errors:
        text_posts = TextPost.objects.filter(user=request.user)
        context['text_posts'] = TextPost.objects.filter(user=request.user).order_by('-date_created')
        return render(request, 'home.html', context)

    user = User.objects.filter(id=user_id)[0]
    text_posts = TextPost.objects.filter(user=user_id)
    context['text_posts'] = text_posts.order_by('-date_created')
    context['text_posts_count'] = len(text_posts)
    context['user'] = user

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



def dislike(request, redirect_name, user_id, text_post_id):
    context = {}
    dislikes = Dislike.objects.all()
    context['dislike_redirect'] = redirect_name

    # for dislike in dislikes:
    #     dislike.delete()

    text_post = TextPost.objects.get(id=text_post_id)

    exists = False
    for dislike in dislikes:
        if (dislike.user == request.user and dislike.post == text_post):
            exists = True

    if not exists:
        dislike = Dislike(user=request.user, post=text_post)
        dislike.save()

    context['dislikes'] = dislikes

    #return context
    #return render(request, 'home.html', context)

    if (redirect_name == 'profile'):
        return redirect(reverse('profile', kwargs={'user_id':user_id}))
    else:
       return redirect(reverse(redirect_name))
    
@login_required
@transaction.atomic
def stream_dislike(request, user_id, text_post_id):
    context = dislike_post(request, user_id, text_post_id)
    context['user'] = request.user
    context['text_posts'] = TextPost.get_posts_without_user(request.user)
    return render(request, 'stream.html', context)

    # return render(request, 'text-post.html', context)

def login_register(request):
    context = {}

    #if request.method == 'GET':
    return render(request, 'login-register.html', context)

def reset_form(request):
    context = {}

    return render(request, 'reset.html', context)

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

    context['reset_message'] = 'You have been sent an email with instructions on how to reset your password.'

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


    # Logs in the new user and redirects to his/her home stream
    # new_user = authenticate(username=request.POST['username'], \
    #                         password=request.POST['password'])
    # login(request, new_user)

    return render(request, 'needs-confirmation.html', context)

    #return redirect(reverse('home'))

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







