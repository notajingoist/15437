# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr_app', '0002_auto_20140920_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=20000)),
                ('user', models.ForeignKey(related_name=b'posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
