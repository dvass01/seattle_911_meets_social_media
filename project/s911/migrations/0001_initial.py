# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('latitude', models.DecimalField(decimal_places=12, max_digits=15)),
                ('longitude', models.DecimalField(decimal_places=12, max_digits=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramLocation',
            fields=[
                ('location_ptr', models.OneToOneField(parent_link=True, to='s911.Location', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=('s911.location',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('data', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, to='s911.Post', serialize=False, auto_created=True, primary_key=True)),
                ('image_url', models.URLField(max_length=100)),
            ],
            options={
            },
            bases=('s911.post',),
        ),
        migrations.CreateModel(
            name='SocrataLocation',
            fields=[
                ('location_ptr', models.OneToOneField(parent_link=True, to='s911.Location', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=('s911.location',),
        ),
        migrations.AddField(
            model_name='post',
            name='location',
            field=models.ForeignKey(to='s911.Location', related_name='posts'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='location',
            field=models.ForeignKey(to='s911.Location', related_name='incidents'),
            preserve_default=True,
        ),
    ]
