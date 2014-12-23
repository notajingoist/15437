# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr_app', '0004_textpost_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textpost',
            name='date_created',
        ),
    ]
