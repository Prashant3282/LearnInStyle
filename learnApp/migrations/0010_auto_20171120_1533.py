# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnApp', '0009_quizgrade_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='info',
            field=models.CharField(max_length=1000000000),
        ),
    ]
