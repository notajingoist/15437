# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr_app', '0014_userprofile_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='blocks',
            field=models.ManyToManyField(related_name=b'blocked_by', to='grumblr_app.UserProfile'),
            preserve_default=True,
        ),
    ]
