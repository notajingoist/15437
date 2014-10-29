# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr_app', '0005_remove_textpost_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='textpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now_add=True),
            preserve_default=True,
        ),
    ]
