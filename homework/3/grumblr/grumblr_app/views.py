from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr_app.models import *

# Create your views here.
# @register.filter(is_safe=True)
# def label_with_classes(value, arg):
#     return value.label_tag(attrs{'class': arg})


@login_required
def home(request):
    context = {}

    return render(request, 'home.html', context)

@login_required
def stream(request):
    context = {}

    return render(request, 'stream.html', context)

@login_required
def profile(request):
    context = {}

    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    context = {}

    return render(request, 'edit-profile.html', context)

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
    context['resetMessage'] = 'You have been sent an email with instructions on how to reset your password.'

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















