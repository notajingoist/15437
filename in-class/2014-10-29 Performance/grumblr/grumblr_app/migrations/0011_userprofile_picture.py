# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr_app', '0010_auto_20141002_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'', upload_to=b'profile-pictures', blank=True),
            preserve_default=True,
        ),
    ]
