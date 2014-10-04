from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	location = models.CharField(max_length=200, default='', blank=True)
	about = models.TextField(max_length=20000, default='', blank=True)

	def __unicode__(self):
		return self.user

	#profile picture FileField
	#followers
	#following
	#dislikes
	#grumbls

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

class Comment(models.Model):
	user = models.ForeignKey(User, related_name='comments') #the commenter
	post = models.ForeignKey(TextPost, related_name='comments') #the post being commented on
	text = models.TextField(max_length=20000)

	def __unicode__(self):
		return self.text

class Dislike(models.Model):
	user = models.ForeignKey(User, related_name='dislikes') #the disliker
	post = models.ForeignKey(TextPost, related_name='dislikes') #the post being disliked
	
	def __unicode__(self):
		return str(self.user.id) + ', ' + str(self.post.id)

#class Comment
#	user = models.ForeignKey(User, related_name='comments')
#	
#	
#class Dislike
#
# update_session_auth_hash(request, user)







