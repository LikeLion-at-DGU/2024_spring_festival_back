from django.urls import path, include
from rest_framework import routers

from .views import BoothViewSet

app_name = 'booth'

booth_router = routers.SimpleRouter(trailing_slash=False)
booth_router.register('booth', BoothViewSet, basename='booth')


urlpatterns = [
    path('', include(booth_router.urls)),
]