"""myappapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from myprofile import views
from myprofile.views import UserCompleteView

router = routers.DefaultRouter()
router.register(r'apt', views.ApartmentView)
router.register(r'up', views.UserView)
router.register(r'aptimages', views.ApartmentImageView)

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^rest-auth/', include('rest_auth.urls')),
                  url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
                  url(r'^account/', include('allauth.urls')),
                  url(r'^', include(router.urls)),
                  url(r'^ucomplete/', UserCompleteView.as_view()),
                  url(r'addapt/(?P<pk>[0-9]+)/$', views.ApartmentUpdateView.as_view()),
                  url(r'addaptlist/(?P<miles>\d+)/(?P<lon>-?\d+\.\d+),(?P<lat>-?\d+\.\d+)/(?P<budget>\d+)/$',
                      views.ApartmentAddListView.as_view()),
                  url(r'addaptlist/$', views.ApartmentAddListView.as_view()),
                  url(r'addroomielist/(?P<miles>\d+)/(?P<lon>-?\d+\.\d+),(?P<lat>-?\d+\.\d+)/$',
                      views.RoomieListView.as_view()),
                  url(r'addroomielist/$', views.RoomieListView.as_view()),
                  url(r'addroomie/(?P<pk>[0-9]+)/$', views.RoomieUpdateView.as_view()),
                  url(
                      r'roomietoroomie/(?P<miles>\d+)/(?P<lon>-?\d+\.\d+),(?P<lat>-?\d+\.\d+)/(?P<userid>\d+)/(?P<budget>\d+)/(?P<k>\d+)/$',
                      views.RoomietoRoomieListView.as_view()),
                  url(
                      r'apttoroomienew/(?P<miles>\d+)/(?P<lon>-?\d+\.\d+),(?P<lat>-?\d+\.\d+)/(?P<userid>\d+)/(?P<budget>\d+)/(?P<k>\d+)/$',
                      views.ApttoRoomieListViewNew.as_view()),

                   url(
                      r'apttoroomie/(?P<miles>\d+)/(?P<lon>-?\d+\.\d+),(?P<lat>-?\d+\.\d+)/(?P<budget>\d+)/(?P<k>\d+)/$',
                      views.ApttoRoomieListView.as_view()),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
