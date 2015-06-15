# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('s911', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='data',
        ),
        migrations.AddField(
            model_name='post',
            name='incident',
            field=models.ForeignKey(to='s911.Incident', default=1, related_name='posts'),
            preserve_default=False,
        ),
    ]
