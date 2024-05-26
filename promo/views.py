from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
# Create your views here.

# 디테일 페이지가 필요치 않으므로 list만 구현
class PromotionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class PromotionBannerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Promotion.objects.filter(
        promotionbannerimage__isnull=False
    )
    serializer_class = PromotionBannerSerializer