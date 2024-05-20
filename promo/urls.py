from django.urls import path, include
from .views import *
from rest_framework import routers

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register(r'promotion', PromotionViewSet, basename='promotion')

second_router = routers.SimpleRouter(trailing_slash=False)
second_router.register(r'promotion-banner', PromotionBannerViewSet, basename='promotion-banner')

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(second_router.urls)),
]