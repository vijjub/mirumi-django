import numpy as np
import random
from scipy.spatial.distance import dice
from django.db.models import Q
from sklearn.feature_extraction import DictVectorizer

from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import D

from myprofile.models import UserProfile, Apartment, Roomie


def roomietoroomie(point, roomieid, budget, miles, k):
    v = DictVectorizer(sparse=False)
    # test_pnt = Point(float(-97.7436994), float(30.2711286))
    pnt = GEOSGeometry(point, srid=4326)
    # roomieid = 287
    # budget = 500
    roomies = Roomie.objects.filter(preferredLocation__distance_lte=(pnt, D(mi=miles)), uCost__gte=budget).values(
        'user_id')
    uprofilesroomies = UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).values('noise', 'foodPreference',
                                                                               'cleanliness', 'gender', 'cooking',
                                                                               'uPets', 'sleep', 'smoking',
                                                                               'socializing', 'alcohol')

    uprofilesroomiesids = map(lambda x: x.id, UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only("id"))
    uprofilesroomiesuserids = map(lambda x: x.user_id, UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only("user_id"))
    RD = v.fit_transform(uprofilesroomies)
    profilecount = len(RD)
    distmatrix = np.zeros((profilecount, profilecount))

    for i in range(profilecount):
        for j in range(profilecount):
            cooking = abs(RD[i][3] - RD[j][4]) / 7
            firstpart = dice(RD[i][0:3], RD[j][0:3])
            secondpart = dice(RD[i][4:], RD[j][4:])
            dist = (cooking + firstpart + secondpart) / 26
            distmatrix[i][j] = dist

    ids = uprofilesroomiesuserids.index(roomieid)
    distmatrixnewsorted = np.argsort(distmatrix[ids])[1:k+1]
    result = []

    for i in range(len(distmatrixnewsorted)):
        result.append(uprofilesroomiesuserids[distmatrixnewsorted[i]])

    newresult = Roomie.objects.filter(user__pk__in=result)
    return newresult


def roomietoroomieall(point, roomieid, budget, miles):
    v = DictVectorizer(sparse=False)
    # test_pnt = Point(float(-97.7436994), float(30.2711286))
    pnt = GEOSGeometry(point, srid=4326)
    # roomieid = 287
    # budget = 500
    roomies = Roomie.objects.filter(preferredLocation__distance_lte=(pnt, D(mi=miles)), uCost__gte=budget).values(
        'user_id')
    uprofilesroomies = UserProfile.objects.filtee(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).values('noise', 'foodPreference',
                                                                               'cleanliness', 'gender', 'cooking',
                                                                               'uPets', 'sleep', 'smoking',
                                                                               'socializing', 'alcohol')

    uprofilesroomiesids = map(lambda x: x.id, UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only("id"))
    uprofilesroomiesuserids = map(lambda x: x.user_id, UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only("user_id"))
    RD = v.fit_transform(uprofilesroomies)
    profilecount = len(RD)
    distmatrix = np.zeros((profilecount, profilecount))

    for i in range(profilecount):
        for j in range(profilecount):
            cooking = abs(RD[i][3] - RD[j][4]) / 7
            firstpart = dice(RD[i][0:3], RD[j][0:3])
            secondpart = dice(RD[i][4:], RD[j][4:])
            dist = (cooking + firstpart + secondpart) / 26
            distmatrix[i][j] = dist

    ids = uprofilesroomiesuserids.index(roomieid)
    distmatrixnewsorted = np.argsort(distmatrix[ids])[1:]
    result = []

    for i in range(len(distmatrixnewsorted)):
        result.append(uprofilesroomiesuserids[distmatrixnewsorted[i]])

    newresult = Roomie.objects.filter(user__pk__in=result)
    return newresult


def apttoroomie(point, roomieid, budget, miles, k):
    v = DictVectorizer(sparse=False)
    # test_pnt = Point(float(-97.7436994), float(30.2711286))
    pnt = GEOSGeometry(point, srid=4326)
    # roomieid = 422
    # budget = 500
    roomies = Roomie.objects.filter(preferredLocation__distance_lte=(pnt, D(mi=miles)), uCost__gte=budget).values(
        'user_id')
    uprofilesroomies = UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).values('noise',
                                                                                                         'foodPreference',
                                                                                                         'cleanliness',
                                                                                                         'gender',
                                                                                                         'cooking',
                                                                                                         'uPets',
                                                                                                         'sleep',
                                                                                                         'smoking',
                                                                                                         'socializing',
                                                                                                         'alcohol')

    uprofilesroomiesids = map(lambda x: x.id,
                              UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only("id"))
    uprofilesroomiesuserids = map(lambda x: x.user_id,
                                  UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only(
                                      "user_id"))
    RD = v.fit_transform(uprofilesroomies)
    profilecount = len(RD)
    distmatrix = np.zeros((profilecount, profilecount))

    for i in range(profilecount):
        for j in range(profilecount):
            cooking = abs(RD[i][3] - RD[j][3]) / 7
            firstpart = dice(RD[i][0:3], RD[j][0:3])
            secondpart = dice(RD[i][4:], RD[j][4:])
            dist = (cooking + firstpart + secondpart) / 26
            distmatrix[i][j] = dist

    ids = uprofilesroomiesuserids.index(roomieid)
    distmatrixnewsorted = np.argsort(distmatrix[ids])[1:k+1]
    result = []

    for i in range(len(distmatrixnewsorted)):
        result.append(uprofilesroomiesuserids[distmatrixnewsorted[i]])

    newresult = Roomie.objects.filter(user__pk__in=result)
    return newresult


def apttoroomieall(point, roomieid, budget, miles):
    v = DictVectorizer(sparse=False)
    # test_pnt = Point(float(-97.7436994), float(30.2711286))
    pnt = GEOSGeometry(point, srid=4326)
    # roomieid = 422
    # budget = 500
    roomies = Roomie.objects.filter(preferredLocation__distance_lte=(pnt, D(mi=miles)), uCost__gte=budget).values(
        'user_id')
    uprofilesroomies = UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).values('noise',
                                                                                                         'foodPreference',
                                                                                                         'cleanliness',
                                                                                                         'gender',
                                                                                                         'cooking',
                                                                                                         'uPets',
                                                                                                         'sleep',
                                                                                                         'smoking',
                                                                                                         'socializing',
                                                                                                         'alcohol')

    uprofilesroomiesids = map(lambda x: x.id,
                              UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only("id"))
    uprofilesroomiesuserids = map(lambda x: x.user_id,
                                  UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only(
                                      "user_id"))
    RD = v.fit_transform(uprofilesroomies)
    profilecount = len(RD)
    distmatrix = np.zeros((profilecount, profilecount))

    for i in range(profilecount):
        for j in range(profilecount):
            cooking = abs(RD[i][3] - RD[j][3]) / 7
            firstpart = dice(RD[i][0:3], RD[j][0:3])
            secondpart = dice(RD[i][4:], RD[j][4:])
            dist = (cooking + firstpart + secondpart) / 26
            distmatrix[i][j] = dist

    ids = uprofilesroomiesuserids.index(roomieid)
    distmatrixnewsorted = np.argsort(distmatrix[ids])[1:]
    result = []

    for i in range(len(distmatrixnewsorted)):
        result.append(uprofilesroomiesuserids[distmatrixnewsorted[i]])

    newresult = Roomie.objects.filter(user__pk__in=result)
    return newresult

# def mainalgorithm():
#     v = DictVectorizer(sparse=False)
#     test_pnt = Point(float(-97.7436994), float(30.2711286))
#     pnt = GEOSGeometry(test_pnt, srid=4326)
#     roomieid = 422
#     budget = 2000
#     roomies = Roomie.objects.filter(preferredLocation__distance_lte=(pnt, D(mi=100)), uCost__gte=budget).values(
#         'user_id')
#     uprofilesroomies = UserProfile.objects.filter(user__pk__in=roomies).values('noise','foodPreference', 'cleanliness',
#                                                                                                          'gender',
#                                                                                                          'cooking',
#                                                                                                          'uPets',
#                                                                                                          'sleep',
#                                                                                                          'smoking',
#                                                                                                          'socializing',
#                                                                                                          'alcohol')
#
#     uprofilesroomiesids = map(lambda x: x.id,
#                               UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only("id"))
#     uprofilesroomiesuserids = map(lambda x: x.user_id,
#                                   UserProfile.objects.filter(Q(user__pk__in=roomies) | Q(user__pk=roomieid)).only(
#                                       "user_id"))
#     RD = v.fit_transform(uprofilesroomies)
#     profilecount = len(RD)
#     distmatrix = np.zeros((profilecount, profilecount))
#
#     for i in range(profilecount):
#         for j in range(profilecount):
#             cooking = abs(RD[i][3] - RD[j][3]) / 7
#             firstpart = dice(RD[i][0:3], RD[j][0:3])
#             secondpart = dice(RD[i][4:], RD[j][4:])
#             dist = (cooking + firstpart + secondpart) / 26
#             distmatrix[i][j] = dist
#
#     uniquedistances = np.unique(distmatrix)
#     divisor = 2
#     midpoint = len(uniquedistances) / divisor
#     alpha = uniquedistances[midpoint]
#     k = 5
#     newresult = []
#     for i in range(profilecount):
#         fresult = grpdia(uniquedistances, distmatrix[i], k, midpoint, divisor)
#
#         # if len(result) == 0:
#         #     divisor *= 2
#         #     midpoint += len(uniquedistances) / divisor
#         #     aplha = uniquedistances[midpoint]
#         #     result = grpdia(alpha,distmatrix[i],k)
#         #
#         # else:
#         #     newresult = result
#         newresult = fresult
#         break
#     return newresult


def grpdia(uniquedistances, uidist, k, midpoint, divisor):
    flist = []
    divisor *= 2
    aplha = uniquedistances[midpoint]
    for i in range(len(uidist)):
        if uidist[i] <= aplha:
            flist.append(i)
    try:
        result = random.sample(flist, k)
        return result

    except ValueError:
        midpoint += len(uniquedistances) / divisor
        result = grpdia(uniquedistances, uidist, k, midpoint, divisor)

    return result


def mainalgorithm(point, budget, miles, k                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ):
    v = DictVectorizer(sparse=False)
    # test_pnt = Point(float(-97.7436994), float(30.2711286))
    pnt = GEOSGeometry(point, srid=4326)
    # k = 5
    # budget = 300
    roomies = Roomie.objects.filter(preferredLocation__distance_lte=(pnt, D(mi=miles)), uCost__gte=budget).values(
        'user_id')
    uprofilesroomies = UserProfile.objects.filter(user__pk__in=roomies).values('noise', 'foodPreference', 'cleanliness',
                                                                               'gender',
                                                                               'cooking',
                                                                               'uPets',
                                                                               'sleep',
                                                                               'smoking',
                                                                               'socializing',
                                                                               'alcohol')

    uprofilesroomiesids = map(lambda x: x.user_id,
                              UserProfile.objects.filter(Q(user__pk__in=roomies)).only("user_id"))

    ## IF result < k
    roomiesall = Roomie.objects.filter(preferredLocation__distance_lte=(pnt, D(mi=100))).values(
        'user_id')

    uprofilesroomiesall = map(lambda x: x.id,
                              UserProfile.objects.filter(Q(user__pk__in=roomiesall)).only("id"))

    if len(roomies) < k:
        return []

    RD = v.fit_transform(uprofilesroomies)
    profilecount = len(RD)
    distmatrix = np.zeros((profilecount, profilecount))

    for i in range(profilecount):
        for j in range(profilecount):
            cooking = abs(RD[i][3] - RD[j][3]) / 7
            firstpart = dice(RD[i][0:3], RD[j][0:3])
            secondpart = dice(RD[i][4:], RD[j][4:])
            dist = (cooking + firstpart + secondpart) / 26
            distmatrix[i][j] = dist

    uniquedistances = np.unique(distmatrix)
    divisor = 2
    midpoint = len(uniquedistances) / divisor
    alpha = uniquedistances[midpoint]

    newresult = []
    for i in range(profilecount):
        flist = []
        divisor *= 2
        lis = distmatrix[i]
        for j in range(len(lis)):
            if lis[j] <= alpha:
                flist.append(j)
        try:
            result = random.sample(flist, k)

        except ValueError:
            midpoint += len(uniquedistances) / divisor
            continue

    for i in range(len(result)):
        newresult.append(uprofilesroomiesids[result[i]])

    fresult = Roomie.objects.filter(user__pk__in=newresult)
    return fresult
