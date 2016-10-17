# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-17 15:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='actor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_Performer', to=settings.AUTH_USER_MODEL, verbose_name='Perfomer'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_Actor', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='log',
            name='action_resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Action_Resource', verbose_name='Action_Resource'),
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Actor'),
        ),
        migrations.AddField(
            model_name='action_resource',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Action', verbose_name='Action_Applied'),
        ),
        migrations.AddField(
            model_name='action_resource',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Resource', verbose_name='Resource'),
        ),
    ]
