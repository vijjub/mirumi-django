from __future__ import unicode_literals

import datetime
#from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='uProfile')
    age = models.IntegerField(validators=[MinValueValidator(17), MaxValueValidator(130)])
    gender = models.CharField(max_length=1)
    profileImg = models.ImageField(upload_to='profileImg/', null=True, blank=True)
    # uCost = models.IntegerField()
    cooking = models.PositiveIntegerField()
    foodPreference = models.CharField(max_length=255)
    cleanliness = models.CharField(max_length=255)
    smoking = models.BooleanField()
    alcohol = models.BooleanField(default=False)
    noise = models.CharField(max_length=255)
    socializing = models.CharField(max_length=255)
    uPets = models.BooleanField(default=True)
    sleep = models.CharField(default='Early Bird',max_length=255)
#    dateMovin = models.DateField(null=True, blank=True, default=None)
#    otherRoomie = models.BooleanField(default=False)
#    duration = models.CharField(null=True, blank=True, max_length=255)
#    preferredLocation = models.PointField(null=True)


class Roomie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='roomie')
    otherRoomie = models.BooleanField(default=False)
    roomie = models.BooleanField(default=False)
    roomieDesc = models.CharField(max_length=255)
    duration = models.CharField(null=True, blank=True, max_length=255)
    preferredLocation = models.PointField(null=True)
    dateMovin = models.DateField(null=True, blank=True, default=None)
    roomieGender = models.CharField(max_length=1)
    roomieGenderOther = models.BooleanField(default=False)##remove it
    roomieAgeMin = models.IntegerField(validators=[MinValueValidator(17), MaxValueValidator(130)],default=17)
    roomieAgeMax = models.IntegerField(validators=[MinValueValidator(17), MaxValueValidator(130)],default=50)
    objects = models.GeoManager()
    uCost = models.IntegerField()

    def __unicode__(self):
        return str(self.roomieDesc)


class Apartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uApartments')
    address = models.TextField()
    desc = models.CharField(max_length=255)
    rooms = models.PositiveIntegerField()
    rent = models.PositiveIntegerField()
    utilities = models.PositiveIntegerField(default=0)
    vacancy = models.PositiveIntegerField()
    internet = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    dateMovin = models.DateField(null=True)
    duration = models.CharField(null=True, max_length=255)
    objects = models.GeoManager()
    placeType = models.CharField(max_length=255)
    pool = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    location = models.PointField(null=True, srid=4326)
    gender = models.CharField(max_length=1)
    ageMin = models.IntegerField(validators=[MinValueValidator(17), MaxValueValidator(130)],default=17)
    ageMax = models.IntegerField(validators=[MinValueValidator(17), MaxValueValidator(130)],default=50)
    deposit = models.IntegerField(default=0)
    music = models.BooleanField(default=False)
    guests = models.BooleanField(default=False)
    drugs = models.BooleanField(default=False)
    lateNights = models.BooleanField(default=False)
    washer = models.BooleanField(default=False)
    dryer = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)
    closet = models.BooleanField(default=False)
    airConditioner = models.BooleanField(default=False)
    heater = models.BooleanField(default=False)
    hasPet = models.BooleanField(default=False)
    # occupant = models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = "Apartments"

    def __unicode__(self):
        return str(self.desc)


class ApartmentImages(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='aptImages',null=True,blank=True)
    image = models.ImageField(upload_to='aptImages/')

    class Meta:
        verbose_name_plural = "Apartment Images"





