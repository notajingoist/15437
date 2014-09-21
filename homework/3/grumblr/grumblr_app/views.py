from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr_app.models import *

# Create your views here.
@login_required
def home(request):
    context = {}
    
    text_posts = TextPost.objects.filter(user=request.user)
    context['text_posts'] = text_posts.filter(user=request.user).order_by('-date_created')

    return render(request, 'home.html', context)

@login_required
def stream(request):
    context = {}
    context['user'] = request.user

    text_posts = TextPost.objects.all()
    context['text_posts'] = text_posts.order_by('-date_created')

    return render(request, 'stream.html', context)

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
    context['user'] = user

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    context['user_profile'] = user_profile

    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    context = {}
    user = request.user
    #user_profile = user.userprofile#UserProfile.objects.get_or_create(user=user)
    #context['user_profile'] = user_profile

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

    return render(request, 'home.html', context)

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
    context['reset_message'] = 'You have been sent an email with instructions on how to reset your password.'

    return render(request, 'reset.html', context)

def register_form(request):
    context = {}

    return render(request, 'register.html', context) 

def register(request):
    context = {}
    errors = []
    context['errors'] = errors

    # return render(request, 'login-register.html', context)

    if request.method == 'GET':
        return render(request, 'login-register.html', context)

    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'email' in request.POST or not request.POST['email']:
        errors.append('Email is required.')
    else:
        # Save the email in the request context to re-fill the email
        # field in case the form has errrors
        context['email'] = request.POST['email']

    if not 'password-1' in request.POST \
        or not request.POST['password-1']:
        errors.append('Password is required.')
    if not 'password-2' in request.POST \
        or not request.POST['password-2']:
        errors.append('Confirm password is required.')

    if 'password-1' in request.POST \
        and 'password-2'in request.POST \
        and request.POST['password-1'] \
        and request.POST['password-2'] \
        and request.POST['password-1'] \
        != request.POST['password-2']:
        errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if len(User.objects.filter(email = request.POST['email'])) > 0:
        errors.append('Email is already taken.')

    if errors:
        return render(request, 'register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        email=request.POST['email'], \
                                        password=request.POST['password-1'])
    new_user.save()

    # Logs in the new user and redirects to his/her home stream
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password-1'])
    login(request, new_user)
    return redirect('/')
