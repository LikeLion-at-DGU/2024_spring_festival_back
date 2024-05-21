from rest_framework import serializers
from .models import *
from datetime import datetime

def trans_datetime_to_str(instance):
    start_at = instance.start_at
    end_at = instance.end_at

    # 시간 str
    start_time = start_at.strftime('%H:%M')
    end_time = end_at.strftime('%H:%M')

    return f"{start_time} ~ {end_time}"

class PerformanceSerializer(serializers.ModelSerializer):
    
    during = serializers.SerializerMethodField()
    is_now = serializers.SerializerMethodField()

    def get_during(self, instance):
        return trans_datetime_to_str(instance)
    
    def get_is_now(self, instance):
        now = datetime.now()
        return instance.start_at <= now <= instance.end_at

    class Meta:
        model = Performance
        fields = [
            'id',
            'operator',
            'location',
            'start_at',
            'end_at',
            'during',
            'date',
            'is_now',
        ]

class ArtistSerializer(serializers.ModelSerializer):
    musics = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_musics(self, instance):
        musics = instance.music_set.all()
        return MusicSerializer(musics, many=True, context = self.context).data
    
    def get_images(self, instance):
        request = self.context.get('request')
        images = instance.artistimage_set.all()
        return [request.build_absolute_uri(image.image.url) for image in images]

    class Meta:
        model = Artist
        fields = [
            'id',
            'name',
            'date',
            'musics',
            'images',
        
        ]

class MusicSerializer(serializers.ModelSerializer):
    album = serializers.SerializerMethodField()

    def get_album(self, instance):
        request = self.context.get('request')
        music_image = instance.musicimage
        if music_image:
            return request.build_absolute_uri(music_image.image.url)
        return None

    class Meta:
        model = Music
        fields = [
            'id',
            'title',
            'ytb_url',
            'album',
        ]

class ArtistImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ArtistImage
        fields = '__all__'

class MusicImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = MusicImage
        fields = '__all__'
