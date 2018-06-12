# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-12 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recorder', '0003_auto_20180612_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earning',
            name='inserted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Eingefügt'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='inserted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Eingefügt'),
        ),
        migrations.AlterField(
            model_name='labourcost',
            name='inserted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Eingefügt'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='inserted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Eingefügt'),
        ),
        migrations.AlterField(
            model_name='materialcost',
            name='inserted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Eingefügt'),
        ),
        migrations.AlterField(
            model_name='project',
            name='inserted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Eingefügt'),
        ),
    ]
