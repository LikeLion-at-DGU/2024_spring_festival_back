# serializers.py
from rest_framework import serializers
from .models import Promotion, PromotionImage, PromotionBannerImage

class PromotionImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = PromotionImage
        fields = ['image']

class PromotionBannerImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = PromotionBannerImage
        fields = ['image']

class PromotionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    def get_image(self, instance):
        request = self.context.get('request')
        promotion_image = instance.promotionimage
        if promotion_image:
            return request.build_absolute_uri(promotion_image.image.url)
        return None

    class Meta:
        model = Promotion
        fields = ['id', 'title', 'description', 'insta_url', 'image']

class PromotionBannerSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()

    def get_banner(self, instance):
        request = self.context.get('request')
        promotion_banner_image = instance.promotionbannerimage
        if promotion_banner_image:
            return request.build_absolute_uri(promotion_banner_image.image.url)
        return None
    
    class Meta:
        model = Promotion
        fields = ['id', 'insta_url', 'banner']