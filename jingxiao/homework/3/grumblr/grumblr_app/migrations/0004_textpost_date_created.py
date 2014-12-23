# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr_app', '0003_auto_20140920_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='textpost',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
