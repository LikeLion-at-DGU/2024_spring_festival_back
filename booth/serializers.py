from rest_framework import serializers
from.models import Booth, BoothImage, BoothLike
from datetime import datetime, date

def trans_datetime_to_str(instance):
    start_at = instance.start_at
    end_at = instance.end_at

    # 요일 str
    days = ['월', '화', '수', '목', '금', '토', '일']
    start_day = start_at.weekday()
    end_day = end_at.weekday()

    if start_day <= end_day:
        day_range = days[start_day:end_day + 1]
    else:
        day_range = days[start_day:] + days[:end_day + 1]

    day_str = ', '.join(day_range)

    # 시간 str
    start_time = start_at.strftime('%H:%M')
    end_time = end_at.strftime('%H:%M')

    return f"({day_str}) {start_time} ~ {end_time}"

class BoothImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = BoothImage
        fields = ['image']

class BoothListSerializer(serializers.ModelSerializer):
    like_cnt = serializers.IntegerField()
    thumbnail = serializers.SerializerMethodField()
    during = serializers.SerializerMethodField()

    def get_thumbnail(self, instance):
        request = self.context.get('request')
        first_image = instance.boothimages.first()
        if first_image:
            thumbnail_url = request.build_absolute_uri(first_image.image.url)
            return thumbnail_url
        return None
    
    def get_during(self, instance):
        return trans_datetime_to_str(instance)
    
    class Meta:
        model = Booth
        fields = [
            'id',
            'name',
            'thumbnail',
            'operator',
            'location',
            'like_cnt',
            'during',
        ]

class BoothSerializer(serializers.ModelSerializer):
    like_cnt = serializers.IntegerField()
    is_liked = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    during = serializers.SerializerMethodField()

    def get_is_liked(self, instance):
        return None

    def get_during(self, instance):
        return trans_datetime_to_str(instance)    
    
    def get_images(self, instance):
        request=self.context.get('request')
        boothimage=instance.boothimages.all().order_by('id')
        try:
            booth_image_serializer=BoothImageSerializer(boothimage, many=True)
            outcome = []
            for data in booth_image_serializer.data:
                image_url = request.build_absolute_uri(data["image"])
                outcome.append(image_url)
            return outcome
        
        except:
            return None

    class Meta:
        model = Booth
        fields = [
            'id',
            'name',
            'description',
            'operator',
            'location',
            'during',
            'like_cnt',
            'is_liked',
            'images',
        ]

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoothLike
        fields = ['id', 'booth', 'key']