# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-10 03:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('h5p', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='h5p_content_user_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField()),
                ('content_main_id', models.PositiveIntegerField()),
                ('sub_content_id', models.PositiveIntegerField()),
                ('data_id', models.CharField(max_length=127)),
                ('timestamp', models.PositiveIntegerField()),
                ('data', models.TextField()),
                ('preloaded', models.PositiveSmallIntegerField(null=True)),
                ('delete_on_content_change', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'db_table': 'h5p_content_user_data',
            },
        ),
        migrations.CreateModel(
            name='h5p_contents',
            fields=[
                ('content_id', models.AutoField(help_text='Identifier of the content', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('json_contents', models.TextField(help_text='The content in JSON format')),
                ('embed_type', models.CharField(default='', max_length=127)),
                ('disable', models.PositiveIntegerField(default=0)),
                ('main_library_id', models.PositiveIntegerField(help_text='The library we first instanciate for this content')),
                ('content_type', models.CharField(help_text='Content type as defined in h5p.json', max_length=127, null=True)),
                ('author', models.CharField(max_length=127, null=True)),
                ('license', models.CharField(blank=True, max_length=7, null=True)),
                ('meta_keywords', models.TextField(blank=True, null=True)),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('filtered', models.TextField(help_text='Filtered version of json_contents')),
                ('slug', models.CharField(help_text='Human readable content identifier that is unique', max_length=127)),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Contents',
                'db_table': 'h5p_contents',
                'ordering': ['title', 'author', 'content_id'],
            },
        ),
        migrations.CreateModel(
            name='h5p_contents_libraries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.PositiveIntegerField()),
                ('library_id', models.PositiveIntegerField()),
                ('dependency_type', models.CharField(default='preloaded', max_length=31)),
                ('drop_css', models.PositiveSmallIntegerField(default=0)),
                ('weight', models.PositiveIntegerField(default=999999)),
            ],
            options={
                'db_table': 'h5p_contents_libraries',
            },
        ),
        migrations.CreateModel(
            name='h5p_counters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=63)),
                ('library_name', models.CharField(max_length=127)),
                ('library_version', models.CharField(max_length=31)),
                ('num', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'h5p_counters',
            },
        ),
        migrations.CreateModel(
            name='h5p_events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField(help_text='Identifier of the user who caused this event')),
                ('created_at', models.IntegerField()),
                ('type', models.CharField(help_text='Type of the event. If it concerns a library, a content or a user', max_length=63)),
                ('sub_type', models.CharField(help_text='Action of the event. Example : Create, Delete, Edit...', max_length=63)),
                ('content_id', models.PositiveIntegerField(help_text='If not 0, identifier of the content affected by this event')),
                ('content_title', models.CharField(help_text='If not blank, title of the content affected by this event', max_length=255)),
                ('library_name', models.CharField(help_text='If not blank, name of the library affected by this event', max_length=127)),
                ('library_version', models.CharField(help_text='If not blank, version of the library affected by this event', max_length=31)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'db_table': 'h5p_events',
                'ordering': ['created_at', 'type', 'sub_type'],
            },
        ),
        migrations.CreateModel(
            name='h5p_libraries',
            fields=[
                ('library_id', models.AutoField(help_text='Identifier of the library', primary_key=True, serialize=False)),
                ('machine_name', models.CharField(default='', help_text='Full name of the library', max_length=127)),
                ('title', models.CharField(default='', help_text='Short name of the library', max_length=255)),
                ('major_version', models.PositiveIntegerField()),
                ('minor_version', models.PositiveIntegerField()),
                ('patch_version', models.PositiveIntegerField()),
                ('runnable', models.PositiveSmallIntegerField(default=1, help_text='If the library can be started alone (not a dependency) ?')),
                ('fullscreen', models.PositiveSmallIntegerField(default=0, help_text='Display fullscreen button')),
                ('embed_types', models.CharField(blank=True, default='', max_length=255)),
                ('preloaded_js', models.TextField(help_text='List of JavaScript files needed by the library', null=True)),
                ('preloaded_css', models.TextField(help_text='List of Stylesheet files needed by the library', null=True)),
                ('drop_library_css', models.TextField(blank=True, help_text='List of Libraries that should not have CSS included if this library is used', null=True)),
                ('semantics', models.TextField(blank=True, help_text='The semantics definition in JSON format')),
                ('restricted', models.PositiveSmallIntegerField(default=0, help_text='If this library can be used to create new content')),
                ('tutorial_url', models.CharField(blank=True, help_text='URL to a tutorial for this library', max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'Library',
                'verbose_name_plural': 'Libraries',
                'db_table': 'h5p_libraries',
                'ordering': ['machine_name', 'major_version', 'minor_version'],
            },
        ),
        migrations.CreateModel(
            name='h5p_libraries_languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_id', models.PositiveIntegerField()),
                ('language_code', models.CharField(max_length=31)),
                ('language_json', models.TextField(help_text='The translations defined in json format')),
            ],
            options={
                'verbose_name': 'Library-language',
                'verbose_name_plural': 'Libraries-languages',
                'db_table': 'h5p_libraries_languages',
                'ordering': ['language_code', 'library_id'],
            },
        ),
        migrations.CreateModel(
            name='h5p_libraries_libraries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_id', models.PositiveIntegerField()),
                ('required_library_id', models.PositiveIntegerField()),
                ('dependency_type', models.CharField(max_length=31)),
            ],
            options={
                'db_table': 'h5p_libraries_libraries',
            },
        ),
        migrations.CreateModel(
            name='h5p_points',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.PositiveIntegerField(help_text='Identifier of the content having a score')),
                ('uid', models.PositiveIntegerField(help_text='Identifier of the user with this score')),
                ('started', models.PositiveIntegerField(help_text='Timestamp. Indicates when the user started watching the video')),
                ('finished', models.PositiveIntegerField(default=0, help_text='Timestamp. Indicates when the user finished watching the video')),
                ('points', models.PositiveIntegerField(blank=True, help_text='Current point of the user', null=True)),
                ('max_points', models.PositiveIntegerField(blank=True, help_text='Maximum point that the user can have', null=True)),
            ],
            options={
                'verbose_name': 'Score',
                'verbose_name_plural': 'Scores',
                'db_table': 'h5p_points',
                'ordering': ['content_id', 'uid'],
            },
        ),
        migrations.RemoveField(
            model_name='h5p',
            name='url',
        ),
        migrations.AlterUniqueTogether(
            name='h5p_points',
            unique_together=set([('content_id', 'uid')]),
        ),
        migrations.AlterUniqueTogether(
            name='h5p_libraries_libraries',
            unique_together=set([('library_id', 'required_library_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='h5p_libraries_languages',
            unique_together=set([('library_id', 'language_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='h5p_counters',
            unique_together=set([('type', 'library_name', 'library_version')]),
        ),
        migrations.AlterUniqueTogether(
            name='h5p_contents_libraries',
            unique_together=set([('content_id', 'library_id', 'dependency_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='h5p_content_user_data',
            unique_together=set([('user_id', 'content_main_id', 'sub_content_id', 'data_id')]),
        ),
        migrations.AddField(
            model_name='h5p',
            name='h5p_resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='h5p_actual_content', to='h5p.h5p_contents', verbose_name='H5P content'),
        ),
    ]
