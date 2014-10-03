# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20141001_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='expected_calories',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name=b'userprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
