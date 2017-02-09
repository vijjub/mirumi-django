import csv

from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry

from myprofile.models import UserProfile, Roomie, Apartment
from django.db import IntegrityError
from django.contrib.gis.geos import Point
from django.conf import settings

settings.configure()

import sys,os
home = "/home/vijjub/Documents/Django/myappapi/"
sys.path.append(home)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

members = open('myprofile/roomiesMirumy2.csv', "rU")
data = csv.reader(members)

default_password = 'password123'
count =0
for row in data:
    if count == 0:
        count = count +1
        continue
    username = row[0]
    user = User.objects.create_user(username,password=default_password)
    user.is_staff = False
    user.save()
    profile = UserProfile(user_id=user.id)
    profile.age = row[1]
    profile.gender = row[2]
    profile.cooking = row[16]
    profile.foodPreference = row[19]
    profile.cleanliness = row[4]
    profile.smoking = row[3]
    if row[13] == 'TRUE':
        profile.alcohol = True
    else:
        profile.alcohol = False
    profile.noise = row[14]
    profile.socializing = row[15]
    profile.uPets = row[5]
    profile.sleep= row[12]
    profile.save()
    roomie = Roomie(user_id=user.id)
    roomie.otherRoomie = True
    roomie.roomie = True
    roomie.roomieDesc = "Looking for a Roommate"
    roomie.duration = row[7]
    roomie.dateMovin = row[8]
    roomie.roomieGender = row[10]
    roomie.roomieGenderOther = True
    roomie.roomieAgeMin = row[20]
    roomie.roomieAgeMax = row[21]
    roomie.uCost = row[6]
    point = Point(float(row[18]),float(row[17]))
    roomie.preferredLocation = GEOSGeometry(point,srid=4326)
    roomie.save()


for row in data:
    if count == 0:
        count = count +1
        continue
    username = row[0]
    user = User.objects.create_user(username,password=default_password)
    user.is_staff = False
    user.save()
    profile = UserProfile(user_id=user.id)
    profile.age = row[1]
    profile.gender = row[2]
    profile.cooking = row[16]
    profile.foodPreference = row[19]
    profile.cleanliness = row[4]
    profile.smoking = row[3]
    if row[13] == 'TRUE':
        profile.alcohol = True
    else:
        profile.alcohol = False
    profile.noise = row[14]
    profile.socializing = row[15]
    profile.uPets = row[5]
    profile.sleep= row[12]
    profile.save()
    roomie = Roomie(user_id=user.id)
    roomie.otherRoomie = True
    roomie.roomie = True
    roomie.roomieDesc = "Looking for a Roommate"
    roomie.duration = row[7]
    roomie.dateMovin = row[8]
    roomie.roomieGender = row[10]
    roomie.roomieGenderOther = True
    roomie.roomieAgeMin = row[20]
    roomie.roomieAgeMax = row[21]
    roomie.uCost = row[6]
    point = Point(float(row[18]),float(row[17]))
    roomie.preferredLocation = GEOSGeometry(point,srid=4326)
    roomie.save()

apartments = open("myprofile/Apartments2.csv")
aptdata = csv.reader(apartments)
count =0
for row in aptdata:
    if count == 0:
        count = count +1
        continue
    try:
        username = row[0]
        user = User.objects.create_user(username,password=default_password)
        user.is_staff = False
        user.save()
        profile = UserProfile(user_id=user.id)
        profile.age = row[1]
        profile.gender = row[2]
        profile.cooking = row[45]
        profile.foodPreference = row[48]
        profile.cleanliness = row[4]
        profile.smoking = row[3]
        profile.alcohol = row[42]
        profile.noise = row[29]
        profile.socializing = row[44]
        profile.uPets = row[14]
        profile.sleep= row[41]
        profile.save()
        apartment = Apartment()
        apartment.user = User.objects.get(id=user.id)
        apartment.address = row[13]
        apartment.desc =row[13]
        apartment.rooms =row[20]
        apartment.rent =row[5]
        apartment.utilities = 0
        apartment.vacancy = row[21]
        apartment.internet = row[22]
        apartment.gym = row[23]
        apartment.pets = row[19]
        apartment.smoking =row[17]
        apartment.dateMovin =row[8]
        apartment.duration =row[7]
        apartment.placeType =row[24]
        apartment.pool =row[25]
        apartment.wifi =row[26]
        apartment.gender = row[16]
        apartment.ageMin = row[27]
        apartment.ageMax = row[28]
        apartment.deposit = row[6]
        apartment.music = row[29]
        apartment.guests = row[30]
        apartment.drugs = row[31]
        apartment.lateNights = row[32]
        apartment.washer = row[33]
        apartment.dryer =row[34]
        apartment.furnished =row[35]
        apartment.kitchen =row[36]
        apartment.closet =row[37]
        apartment.airConditioner =row[38]
        apartment.heater =row[39]
        apartment.hasPet =row[14]
        point = Point(float(row[47]),float(row[46]))
        apartment.location = GEOSGeometry(point,srid=4326)
        apartment.save()
    except IntegrityError:
        continue





