from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}

    return render(request, 'home.html', context)


def stream(request):
    context = {}

    return render(request, 'stream.html', context)


def profile(request):
    context = {}

    return render(request, 'profile.html', context)


def edit_profile(request):
    context = {}

    return render(request, 'edit-profile.html', context)

def login_register(request):
    context = {}

    return render(request, 'login-register.html', context)


def text_post(request):
    context = {}

    return render(request, 'text-post.html', context)


