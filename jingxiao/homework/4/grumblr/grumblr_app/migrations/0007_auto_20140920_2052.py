# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr_app', '0006_textpost_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textpost',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
        ),
    ]
