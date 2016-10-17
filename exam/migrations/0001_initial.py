# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-17 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=300, verbose_name='Answer')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': 'Answers',
                'verbose_name': 'Answer',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courses.Activity')),
                ('begin_date', models.DateField(verbose_name='Begin of Course Date')),
            ],
            options={
                'verbose_name_plural': 'Exams',
                'verbose_name': 'Exam',
            },
            bases=('courses.activity',),
        ),
        migrations.AddField(
            model_name='answer',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='exam.Exam', verbose_name='Answers'),
        ),
    ]
