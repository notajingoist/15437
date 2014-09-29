from django import forms

from django.contrib.auth.models import User
from models import *

class ResetForm(forms.Form):
    email = forms.CharField(max_length = 200, widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))

    def clean(self):
        cleaned_data = super(ResetForm, self).clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__exact=email):
            raise forms.ValidationError('This email does not exist.')
        return email


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    username = forms.CharField(max_length=20, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(max_length=200, label='Email', widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))
    password = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}))
    password2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}))  

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords did not match.')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError('Username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError('Email is already taken.')
        return email

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data.get('username'), \
                                            email=self.cleaned_data.get('email'), \
                                            password=self.cleaned_data.get('password'))
        new_user.save()
        user_profile, created = UserProfile.objects.get_or_create(user=new_user)
        user_profile.save()
        return new_user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()

    first_name = forms.CharField(max_length=20, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=20, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(max_length=200, label='Email', widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))
    location = forms.CharField(max_length=200, label='Location', widget=forms.TextInput(attrs={'placeholder': 'The Universe'}))
    about = forms.CharField(max_length=200, label='About', widget=forms.Textarea(attrs={'placeholder': 'Write a little about yourself...', 'id': 'edit-about-blurb'}))
    password = forms.CharField(max_length=200, label='New Password', widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}))
    password2 = forms.CharField(max_length=200, label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}))  

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords did not match.')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError('Username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError('Email is already taken.')
        return email

    def save(self):
        user_profile, created = UserProfile.objects.get_or_create(user=new_user)
        user_profile.save()

        return new_user

# class TextPostForm(forms.ModelForm):









