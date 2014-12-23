from django import forms

from django.contrib.auth.models import User
from models import *

class TextPostForm(forms.ModelForm):
    class Meta:
        model = TextPost
        fields = ('text',)#text')
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Grumble grumble grumble...', 'class': 'textarea-text-post'})
        }
        error_messages = {
            'text': {
                'required': 'You must grumble about something in your text post!'
            }
        }
    
    def clean(self):
        cleaned_data = super(TextPostForm, self).clean()
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Offer some words of encouragement...or not...', 'class': 'textarea-text-post'})
        }
        labels = {
            'text': 'Comment'
        }
        error_messages = {
            'text': {
                'required': 'You must write something in your comment!'
            }
        }

    # about = forms.CharField(max_length=20000, 
    #                             label='Comment', 
    #                             widget=forms.Textarea(attrs={'placeholder': 'Give some words of encouragement...or not...', 'class': 'textarea-text-post'})),
    
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        return cleaned_data

class ResetForm(forms.Form):
    email = forms.CharField(max_length = 200, widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))

    def clean(self):
        cleaned_data = super(ResetForm, self).clean()
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__exact=email):
            raise forms.ValidationError('This email does not exist.')
        return email


class RegistrationForm(forms.ModelForm):
    bullets_placeholder = u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'
    class Meta:
        bullets_placeholder = u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': bullets_placeholder}),
        }
        error_messages = {
            'username': {
                'required': 'Username is required.'
            },
            'password': {
                'required': 'Password is required.'
            },
        }

    # username = forms.CharField(max_length=20, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(max_length=200, label='Email', 
                                error_messages={'required': 'Email is required.'}, 
                                widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))
    # password = forms.CharField(max_length=200, label='Password', widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}))
    password2 = forms.CharField(max_length=200, label='Confirm Password', 
                                error_messages={'required': 'Password confirmation is required.'}, 
                                widget=forms.PasswordInput(attrs={'placeholder': bullets_placeholder}))  

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
        new_user.is_active = False
        new_user.save()
        
        return new_user


class UserProfileForm(forms.Form):
    # class Meta:
    #     model = UserProfile
    #     fields = ()
    picture = forms.FileField(label='Profile Picture',
                                widget=forms.FileInput(attrs={'id': 'edit-upload-picture', 'class': 'btn-edit-profile btn-submit'}),
                                required=False)

    first_name = forms.CharField(max_length=20, 
                                label='First Name', 
                                widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
                                required=False)
    last_name = forms.CharField(max_length=20, 
                                label='Last Name', 
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
                                required=False)
    username = forms.CharField(max_length=20, 
                                label='Username', 
                                widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(max_length=200, 
                                label='Email', 
                                widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))
    location = forms.CharField(max_length=200, 
                                label='Location', 
                                widget=forms.TextInput(attrs={'placeholder': 'The Universe'}),
                                required=False)
    about = forms.CharField(max_length=200, 
                                label='About', 
                                widget=forms.Textarea(attrs={'placeholder': 'Write a little about yourself...', 'id': 'edit-about-blurb'}),
                                required=False)


    # password = forms.CharField(max_length=200, 
    #                             label='New Password', 
    #                             widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'}))
    # password2 = forms.CharField(max_length=200, 
    #                             label='Confirm Password', 
    #                             widget=forms.PasswordInput(attrs={'placeholder': u'\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'})) 

    # def clean(self):
    #     cleaned_data = super(UserProfileForm, self).clean()
    #     password = cleaned_data.get('password')
    #     password2 = cleaned_data.get('password2')
    #     if password and password2 and password != password2:
    #         raise forms.ValidationError('Passwords did not match.')
    #     return cleaned_data
    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_exists = User.objects.filter(username__exact=username)
        if user_exists and self.initial['username'] != username:
            raise forms.ValidationError('Username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email__exact=email)
        if email_exists and self.initial['email'] != email:
            raise forms.ValidationError('Email is already taken.')
        return email


    def save(self, user_instance, user_profile_instance):
        # user = User.objects.get(username=user_instance.username)
        # user_profile = UserProfile.objects.get(user=)
        user_instance.last_name = self.cleaned_data.get('last_name')
        user_instance.first_name = self.cleaned_data.get('first_name')
        user_instance.username = self.cleaned_data.get('username')
        user_instance.email = self.cleaned_data.get('email')
        # user_instance.password = self.cleaned_data.get('password')
        # user_instance.password2 = self.cleaned_data.get('password2')

        user_profile_instance.location = self.cleaned_data.get('location')
        user_profile_instance.about = self.cleaned_data.get('about')
        user_profile_instance.picture = self.cleaned_data.get('picture')
        
        user_instance.save()
        user_profile_instance.save()
        
        return user_instance
    
        #self.cleaned_data.get('username')
        # for field in self:
        #     if field.has_changed:
        #         user_instance[]

        # if self.has_changed():

        # user_profile, created = UserProfile.objects.get_or_create(user=new_user)
        # user_profile.save()

        # proper way to associate user profile with user?
        # when to create user profile? I keep using this get or create method
        # can i pass multiple model instances to the model form constructor?
        # how to combine user and user profile into the model form?
        # proper way to specify other fields for model form? etc.
        # 

        # return new_user

# class TextPostForm(forms.ModelForm):









