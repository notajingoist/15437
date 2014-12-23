from django.db import models

from django.contrib.auth.models import BaseUserManager

import hashlib
import random
import binascii

class UserManager(BaseUserManager):
    def create_user(self, username, password):
        u = User(username=username)
        u.set_password(password)
        return u
    def create_superuser(self, username, password):
        return self.create_user(username, password)

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateField(auto_now_add=True)

    def set_password(self, password):
        all_algorithms = hashlib.algorithms
        rand_algorithm_index = random.randrange(0, len(all_algorithms))
        algorithm = all_algorithms[rand_algorithm_index]
        iterations = random.randrange(12000, 24000)
        salt = str(random.getrandbits(16))
        h = hashlib.new(algorithm)

        hashed_password = salt + password
        for x in xrange(0, iterations):
            h.update(hashed_password)
            hashed_password = h.hexdigest()

        self.password = algorithm + '$' + str(iterations) + '$' + salt + '$' + hashed_password

    def check_password(self, password):
        delim_count = 0

        algorithm = ''
        iterations = ''
        salt = ''

        curr_part = ''
        i = 0
        while (i < len(self.password)):
            curr_char = self.password[i]
            if (curr_char == '$'):
                delim_count += 1
                if delim_count == 1:
                    algorithm = curr_part
                elif delim_count == 2:
                    iterations = int(curr_part)
                elif delim_count == 3:
                    salt = curr_part
                curr_part = ''
            else: 
                curr_part += curr_char
            i += 1

        hashed_real_password = curr_part
        h = hashlib.new(algorithm)
        hashed_given_password = salt + password
        for x in xrange(0, iterations):
            h.update(hashed_given_password)
            hashed_given_password = h.hexdigest()

        return hashed_given_password == hashed_real_password

    def __unicode__(self):
        return self.username

    # These fields and methods are necessary to use this model with
    # the rest of the Django authentication framework
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def get_short_name(self):
        return self.username
    def get_long_name(self):
        return self.username

class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.text
