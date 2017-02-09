from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Apartment, User, ApartmentImages, Roomie
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from serializers import ApartmentSerializer, UserSerializer, UserCompleteSerializer, AddApartmentSerializer, \
    AptImagesSerializer, RoomieSerializer, RoomieListSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from myprofile.roomietoroomie import roomietoroomie,roomietoroomieall,apttoroomie,apttoroomieall,mainalgorithm



# Create your views here.


class ApartmentView(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = (IsAuthenticated,)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer


class ApartmentImageView(viewsets.ModelViewSet):
    queryset = ApartmentImages.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AptImagesSerializer


class AddApartmentView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddApartmentSerializer


class UserCompleteView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCompleteSerializer

    def get_object(self):
        return self.request.user


class ApartmentAddListView(APIView):

    def get(self, request, miles, lon, lat,budget, format=None):
        pnt1 = Point(float(lon), float(lat))
        pnt = GEOSGeometry(pnt1, srid=4326)
        # apartments = Apartment.objects.all()
        apartments = Apartment.objects.filter(location__distance_lte=(pnt,D(mi=miles)),rent__lte=budget)
        serializer = ApartmentSerializer(apartments, many=True)
        return Response(serializer.data)

    # def get(self, request, format=None):
    #
    #     apartments = Apartment.objects.all()
    #     # apartments = Apartment.objects.filter(location__distance_lte=(pnt,D(mi=miles)))
    #     serializer = AddApartmentSerializer(apartments, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AddApartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomieListView(APIView):

    def get(self,request, miles,lon, lat, format=None):
        pnt1 = Point(float(lon), float(lat))
        pnt = GEOSGeometry(pnt1, srid=4326)
        roomies = Roomie.objects.filter(preferredLocation__distance_lte=(pnt, D(mi=miles)))
        serializer = RoomieListSerializer(roomies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RoomieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomietoRoomieListView(APIView):

    def get(self, request, miles,lon, lat, userid, budget, k, format=None):
        pnt1 = Point(float(lon), float(lat))
        pnt = GEOSGeometry(pnt1, srid=4326)
        roomies = roomietoroomie(pnt, int(userid), int(budget), int(miles), int(k))
        serializer = RoomieListSerializer(roomies, many=True)
        return Response(serializer.data)


class ApttoRoomieListView(APIView):

    # def get(self, request, miles,lon, lat, userid, budget, k, format=None):
    #     pnt1 = Point(float(lon), float(lat))
    #     pnt = GEOSGeometry(pnt1, srid=4326)
    #     roomies = apttoroomie(pnt, int(userid), int(budget), int(miles), int(k))
    #     serializer = RoomieListSerializer(roomies, many=True)
    #     return Response(serializer.data)

    def get(self, request, miles,lon, lat, budget, k, format=None):
        pnt1 = Point(float(lon), float(lat))
        pnt = GEOSGeometry(pnt1, srid=4326)
        roomies = mainalgorithm(pnt, int(budget), int(miles), int(k))
        serializer = RoomieListSerializer(roomies, many=True)
        return Response(serializer.data)

class ApttoRoomieListViewNew(APIView):

    def get(self, request, miles,lon, lat, userid, budget, k, format=None):
        pnt1 = Point(float(lon), float(lat))
        pnt = GEOSGeometry(pnt1, srid=4326)
        roomies = apttoroomie(pnt, int(userid), int(budget), int(miles), int(k))
        serializer = RoomieListSerializer(roomies, many=True)
        return Response(serializer.data)

    # def get(self, request, miles,lon, lat, budget, k, format=None):
    #     pnt1 = Point(float(lon), float(lat))
    #     pnt = GEOSGeometry(pnt1, srid=4326)
    #     roomies = mainalgorithm(pnt, int(budget), int(miles), int(k))
    #     serializer = RoomieListSerializer(roomies, many=True)
    #     return Response(serializer.data)
    #


class ApartmentUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Apartment.objects.get(pk=pk)
        except Apartment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AddApartmentSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AddApartmentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomieUpdateView(APIView):

    def get_object(self,pk):
        try:
            return Roomie.objects.get(pk=pk)
        except Roomie.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        roomie = self.get_object(pk)
        serializer = RoomieSerializer(roomie)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        roomie = self.get_object(pk)
        serializer = RoomieSerializer(roomie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





