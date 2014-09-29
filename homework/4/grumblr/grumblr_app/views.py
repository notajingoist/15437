from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from models import *
from forms import *

# Create your views here.

# home
@login_required
def home(request):
    context = {}
    context['text_posts'] = TextPost.get_posts_from_user(request.user)
    return render(request, 'home.html', context)

# stream
@login_required
def stream(request):
    context = {}
    context['user'] = request.user
    context['text_posts'] = TextPost.get_posts_without_user(request.user)

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
def edit_profile(request):
    context = {}
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    context['user_profile'] = user_profile

    if request.method == 'GET':
        context['form'] = UserProfileForm(instance=request.user)
        return render(request, 'edit-profile.html', context)

    form = UserProfileForm(request.POST, instance=request.user)
    context['form'] = form

    form.save()

    return render(request, 'edit-profile.html', context)

@login_required
def save_profile_changes(request):
    context = {}
    errors = []
    user = request.user
    context['user'] = user
    context['errors'] = errors

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    if 'firstname' in request.POST and request.POST['firstname']:
        user.first_name = request.POST['firstname']
        user.save()

    if 'lastname' in request.POST and request.POST['lastname']:
        user.last_name = request.POST['lastname']
        user.save()
    
    if 'username' in request.POST and request.POST['username']:
        if len(User.objects.filter(username = request.POST['username'])) > 0:
            errors.append('Username is already taken.')
        else:
            user.username = request.POST['username']
            user.save()

    if 'email' in request.POST and request.POST['email']:
        user.email = request.POST['email']
        user.save()

    if 'about' in request.POST and request.POST['about']:
        user_profile.about = request.POST['about']
        user_profile.save()

    if 'location' in request.POST and request.POST['location']:
        user_profile.location = request.POST['location']
        user_profile.save()

    context['user_profile'] = user_profile
    # request.user.userprofile = UserProfile()
    return render(request, 'edit-profile.html', context)

@login_required
def create_text_post(request):
    context = {}
    errors = []

    if not 'text-body' in request.POST or not request.POST['text-body']:
        errors.append('You must grumble about something in your text post!')
    else:
        new_text_post = TextPost(text=request.POST['text-body'], user=request.user)
        new_text_post.save()

    text_posts = TextPost.objects.filter(user=request.user).order_by('-date_created')
    
    context['text_posts'] = text_posts
    context['errors'] = errors

    if len(errors) > 0:
        return render(request, 'text-post.html', context)

    return redirect(reverse('home'))

@login_required
def text_post(request):
    context = {}

    return render(request, 'text-post.html', context)

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
