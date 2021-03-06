# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-28 18:58
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('desc', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('rooms', models.PositiveIntegerField()),
                ('rent', models.PositiveIntegerField()),
                ('utilities', models.PositiveIntegerField(default=0)),
                ('vacancy', models.PositiveIntegerField()),
                ('laundry', models.BooleanField(default=False)),
                ('internet', models.BooleanField(default=False)),
                ('gym', models.BooleanField(default=False)),
                ('pets', models.BooleanField(default=True)),
                ('smoking', models.BooleanField(default=False)),
                ('dateMovin', models.DateField(null=True)),
                ('duration', models.CharField(max_length=255, null=True)),
                ('placeType', models.CharField(max_length=255)),
                ('pool', models.BooleanField(default=False)),
                ('wifi', models.BooleanField(default=False)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uApartments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Apartments',
            },
        ),
        migrations.CreateModel(
            name='ApartmentImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='aptImages/')),
                ('apartment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aptImages', to='myprofile.Apartment')),
            ],
            options={
                'verbose_name_plural': 'Apartment Images',
            },
        ),
        migrations.CreateModel(
            name='Roomie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otherRoomie', models.BooleanField(default=False)),
                ('roomieDesc', models.CharField(max_length=255)),
                ('duration', models.CharField(blank=True, max_length=255, null=True)),
                ('preferredLocation', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('dateMovin', models.DateField(blank=True, default=None, null=True)),
                ('uCost', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='roomie', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(17), django.core.validators.MaxValueValidator(130)])),
                ('gender', models.CharField(max_length=1)),
                ('profileImg', models.ImageField(blank=True, null=True, upload_to='profileImg/')),
                ('cooking', models.PositiveIntegerField()),
                ('foodPreference', models.CharField(max_length=255)),
                ('cleanliness', models.CharField(max_length=255)),
                ('smoking', models.BooleanField()),
                ('alcohol', models.CharField(max_length=255)),
                ('noise', models.CharField(max_length=255)),
                ('socializing', models.CharField(max_length=255)),
                ('uPets', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='uProfile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
