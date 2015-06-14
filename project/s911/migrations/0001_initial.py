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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('location_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to='s911.Location', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to='s911.Post', serialize=False)),
                ('image_url', models.URLField(max_length=100)),
            ],
            options={
            },
            bases=('s911.post',),
        ),
        migrations.CreateModel(
            name='SocrataLocation',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to='s911.Location', serialize=False)),
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
