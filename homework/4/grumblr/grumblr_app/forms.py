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

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.CharField(max_length = 200, widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))
    password1 = forms.CharField(max_length = 200, label='Password', widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}))
    password2 = forms.CharField(max_length = 200, label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
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
# class TextPostForm(forms.ModelForm):