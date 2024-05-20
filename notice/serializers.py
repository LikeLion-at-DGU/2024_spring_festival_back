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

    def get_thumbnail(self, instance):
        request = self.context.get('request')
        notification_image = instance.notificationimage_set.first()
        if notification_image:
            return request.build_absolute_uri(notification_image.image.url)
        return None

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'created_at', 'thumbnail']

# 공지 디테일
class NotificationDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, instance):
        request = self.context.get('request')
        notification_images = instance.notificationimage_set.all().order_by('id')
        return [request.build_absolute_uri(image.image.url) for image in notification_images]

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'created_at', 'images']

# # 공지
# class NotificationSerializer(serializers.ModelSerializer):
#     images = serializers.SerializerMethodField()
    
#     def get_images(self, instance):
#         request = self.context.get('request')
#         notification_images = instance.notificationimage_set.all().order_by('id')
#         try:
#             notification_image_serializer = NotificationImageSerializer(notification_images, many=True)
#             outcome = []
#             for data in notification_image_serializer.data:
#                 image_url = request.build_absolute_uri(data['image'])
#                 outcome.append(image_url)

#             return outcome
#         except:
#             return None
        
#     class Meta:
#         model = Notification
#         fields = ['id', 'title', 'description', 'created_at', 'images']

        