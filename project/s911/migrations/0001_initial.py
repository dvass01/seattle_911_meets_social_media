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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=500)),
                ('clearance_date', models.DateTimeField()),
                ('cad_event_number', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('latitude', models.DecimalField(max_digits=15, decimal_places=12)),
                ('longitude', models.DecimalField(max_digits=15, decimal_places=12)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramLocation',
            fields=[
                ('location_ptr', models.OneToOneField(parent_link=True, to='s911.Location', auto_created=True, primary_key=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, to='s911.Post', auto_created=True, primary_key=True, serialize=False)),
                ('image_url', models.URLField()),
                ('post_url', models.URLField()),
            ],
            options={
            },
            bases=('s911.post',),
        ),
        migrations.CreateModel(
            name='SocrataLocation',
            fields=[
                ('location_ptr', models.OneToOneField(parent_link=True, to='s911.Location', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=('s911.location',),
        ),
        migrations.AddField(
            model_name='post',
            name='incident',
            field=models.ForeignKey(to='s911.Incident', related_name='posts'),
            preserve_default=True,
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
