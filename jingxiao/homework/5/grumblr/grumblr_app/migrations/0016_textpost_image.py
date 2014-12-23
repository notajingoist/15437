# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr_app', '0015_userprofile_blocks'),
    ]

    operations = [
        migrations.AddField(
            model_name='textpost',
            name='image',
            field=models.ImageField(default=b'', upload_to=b'images', blank=True),
            preserve_default=True,
        ),
    ]
