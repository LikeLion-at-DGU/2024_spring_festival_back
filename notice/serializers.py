from rest_framework import serializers
from .models import *

# 공지 이미지
class NotificationImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = NotificationImage
        fields = ['image']

# 공지 리스트
class NotificationListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    def get_thumbnail(self, instance):
        request = self.context.get('request')
        notification_image = instance.notificationimage_set.first()
        if notification_image:
            return request.build_absolute_uri(notification_image.image.url)
        return None
    
    def get_short_description(self, instance):
        if len(instance.description) <= 23:
            return instance.description
        else:
            return instance.description[:23] + "..."

    class Meta:
        model = Notification
        fields = ['id', 'title', 'short_description','description', 'created_at', 'thumbnail', 'insta_url']

# 공지 디테일 <- 삭제 되었음.
# class NotificationDetailSerializer(serializers.ModelSerializer):
#     images = serializers.SerializerMethodField()

#     def get_images(self, instance):
#         request = self.context.get('request')
#         notification_images = instance.notificationimage_set.all().order_by('id')
#         return [request.build_absolute_uri(image.image.url) for image in notification_images]

#     class Meta:
#         model = Notification
#         fields = ['id', 'title', 'description', 'created_at', 'images']
