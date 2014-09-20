from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	location = models.CharField(max_length=200)
	about = models.TextField(max_length=20000)
	#profile picture FileField
	#followers
	#following
	#dislikes
	#grumblrs

class Post(models.Model):
	author = models.ForeignKey(User, related_name='posts')
	text = models.TextField(max_length=20000)
	#type
	#date DateField
	#picture FileField
	#dislikes


