from django.urls import path, include
from rest_framework import routers

from .views import *
timetable_router = routers.SimpleRouter(trailing_slash=False)
timetable_router.register('timetable', TimetableViewSet, basename='timetable')

artist_router = routers.SimpleRouter(trailing_slash=False)
artist_router.register('artist', ArtistViewSet, basename='artist')


urlpatterns = [
    path('', include(timetable_router.urls)),
    path('', include(artist_router.urls)),    
]
