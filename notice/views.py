from django.shortcuts import render
from rest_framework import viewsets, mixins
from .models import *
from .serializers import *
from rest_framework.decorators import action

# class NotificationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     serializer_class = NotificationSerializer
#     queryset = Notification.objects.all()

class NotificationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Notification.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        if self.action == 'retrieve':
            return NotificationDetailSerializer
        return super().get_serializer_class()
