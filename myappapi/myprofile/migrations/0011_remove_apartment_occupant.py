# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-18 07:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myprofile', '0010_apartment_occupant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='occupant',
        ),
    ]
