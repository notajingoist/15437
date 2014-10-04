from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash

from models import *
from forms import *

# Create your views here.

# home
@login_required
def home(request):
    context = {}
    context['text_posts'] = TextPost.get_posts_from_user(request.user)
    context['dislikes'] = request.user.dislikes.all() #Dislike.objects.all()
    context['comment_redirect'] = 'home'
    context['dislike_redirect'] = 'home'

    return render(request, 'home.html', context)

# stream
@login_required
def stream(request):
    context = {}
    context['user'] = request.user
    context['text_posts'] = TextPost.get_posts_without_user(request.user)
    context['comment_redirect'] = 'stream'
    context['dislike_redirect'] = 'stream'
    # context['comments'] = Comment.objects.all()

    return render(request, 'stream.html', context)

@login_required
def search_stream(request):
    context = {}
    errors = []
    context['errors'] = errors
    context['user'] = request.user

    text_posts = TextPost.objects.exclude(user=request.user)

    if 'keyword' in request.GET and request.GET['keyword']:
        context['keyword'] = request.GET['keyword']
        text_posts = text_posts.filter(text__icontains=request.GET['keyword'])

        if len(text_posts) <= 0:
            errors.append('No search results found for ' + request.GET['keyword'])

    context['text_posts'] = text_posts.order_by('-date_created')

    return render(request, 'stream.html', context)

@login_required
def search_home(request):
    context = {}
    errors = []
    context['errors'] = errors
    context['user'] = request.user

    text_posts = TextPost.objects.filter(user=request.user)

    if 'keyword' in request.GET and request.GET['keyword']:
        context['keyword'] = request.GET['keyword']
        text_posts = text_posts.filter(text__icontains=request.GET['keyword'])

        if len(text_posts) <= 0:
            errors.append('No search results found for ' + request.GET['keyword'])

    context['text_posts'] = text_posts.order_by('-date_created')

    return render(request, 'home.html', context)

@login_required
def search_profile(request, user_id):
    context = {}
    errors = []
    context['errors'] = errors

    if len(User.objects.filter(id=user_id)) <= 0:
        errors.append('User does not exist.')

    if errors:
        text_posts = TextPost.objects.filter(user=request.user)
        context['text_posts'] = TextPost.objects.filter(user=request.user).order_by('-date_created')
        return render(request, 'home.html', context)

    user = User.objects.filter(id=user_id)[0]
    text_posts = TextPost.objects.filter(user=user_id)
    context['text_posts_count'] = len(text_posts)
    context['text_posts'] = text_posts.order_by('-date_created')
    context['user'] = user

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    context['user_profile'] = user_profile

    if len(user.email) > 16:
        new_end_index = 13
        context['email_curtailed'] = user.email[:new_end_index]


    if 'keyword' in request.GET and request.GET['keyword']:
        context['keyword'] = request.GET['keyword']
        text_posts = text_posts.filter(text__icontains=request.GET['keyword'])

        if len(text_posts) <= 0:
            errors.append('No search results found for ' + request.GET['keyword'])

    context['text_posts'] = text_posts.order_by('-date_created')

    return render(request, 'profile.html', context)


@login_required
def profile(request, user_id):
    context = {}
    errors = []
    context['errors'] = errors

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

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    context['user_profile'] = user_profile

    if len(user.email) > 16:
        new_end_index = 13
        context['email_curtailed'] = user.email[:new_end_index]

    return render(request, 'profile.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    # errors = []
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # context['errors'] = errors
    context['user'] = user
    context['user_profile'] = user_profile

    initial_user = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'email': user.email,
                    'location': user_profile.location,
                    'about': user_profile.about
                }

    if request.method == 'GET':
        context['form'] = UserProfileForm(initial=initial_user)
        return render(request, 'edit-profile.html', context)

    form = UserProfileForm(request.POST, initial=initial_user)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'edit-profile.html', context)

    form.save(user_instance=request.user, user_profile_instance=user_profile)
    update_session_auth_hash(request, user)

    return render(request, 'edit-profile.html', context)

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
    return redirect(reverse(redirect_name))
    
@login_required
@transaction.atomic
def stream_dislike(request, user_id, text_post_id):
    context = dislike_post(request, user_id, text_post_id)
    context['user'] = request.user
    context['text_posts'] = TextPost.get_posts_without_user(request.user)
    return render(request, 'stream.html', context)

@login_required
@transaction.atomic
def comment(request, redirect_name, user_id, text_post_id):
    context = {}
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
    return redirect(reverse(redirect_name))

@login_required
@transaction.atomic
def text_post(request):
    context = {}
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

    # Logs in the new user and redirects to his/her home stream
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password'])
    login(request, new_user)

    return redirect(reverse('home'))
