from django.db import models
from django.utils import timezone
from datetime import datetime


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

class TextPost(models.Model):
	user = models.ForeignKey(User, related_name='posts')
	text = models.TextField(max_length=20000)
	date_created = models.DateTimeField(auto_now_add=True, default=timezone.now)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_posts_from_user(user):
		return TextPost.objects.filter(user=user).order_by('-date_created')

	@staticmethod
	def get_posts_without_user(user):
		return TextPost.objects.exclude(user=user).order_by('-date_created')
	#type
	#comments
	#dislikes


