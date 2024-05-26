from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, mixins
from django_filters import rest_framework as filters
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class TimetableFilter(filters.FilterSet):
    date = filters.CharFilter(method='filter_by_date_range')
    location = filters.CharFilter(field_name="location", lookup_expr='icontains')
    is_now = filters.BooleanFilter(method='filter_is_now')

    class Meta:
        model = Performance
        fields = ['date', 'location', 'is_now']
        
    def filter_is_now(self, queryset, name, value):
        now = datetime.now()
        if value:
            return queryset.filter(start_at__lte=now, end_at__gte=now)
        return queryset.exclude(start_at__lte=now, end_at__gte=now)
    
    def filter_by_date_range(self, queryset, name, value):
        try:
            day = int(value)

            queryset = queryset.filter(
                Q(start_at__day__lte=day) & Q(end_at__day__gte=day)
            )
            return queryset
        
        except ValueError:
            return queryset.none()
        
class ArtistFilter(filters.FilterSet):
    day = filters.CharFilter(method='filter_by_day')

    def filter_by_day(self, queryset, name, value):
        try:
            day = int(value)
            return queryset.filter(date__day=day)
        
        except ValueError:
            return queryset.none()

    class Meta:
        model = Artist
        fields = ['day']


class TimetableViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    filter_backends = [DjangoFilterBackend]
    filterset_class = TimetableFilter

    def get_queryset(self):
        queryset = Performance.objects.all()
        return queryset
    
    def get_serializer_class(self):
        return PerformanceSerializer

class ArtistViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Artist.objects.all().order_by('id')
    serializer_class = ArtistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArtistFilter

class MusicViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

class isNowPerformanceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    
    serializer_class = NowPerformanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TimetableFilter

    def get_queryset(self):
        queryset = Performance.objects.all()
        return queryset.filter(start_at__lte=datetime.now(), end_at__gte=datetime.now())