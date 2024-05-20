from django.urls import path, include
from rest_framework import routers
from .views import NotificationViewSet

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register(r'notice', NotificationViewSet, basename='notice')

urlpatterns = [
    path("", include(default_router.urls)),
]