from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class GrumblrUser(models.Model):
	user = models.OneToOneField(User)
	location = models.CharField(max_length=200)
	about_me = models.TextField(max_length=20000)
	#profile_picture FileField
	#followers
	#following
	#dislikes

class Post(models.Model):
	author = models.ForeignKey('GrumblrUser', related_name='posts')
	text = models.TextField(max_length=20000)
	#date DateField
	#picture FileField
	#dislikes


