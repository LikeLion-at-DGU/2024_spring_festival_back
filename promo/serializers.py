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
        try:
            promotion_image = instance.promotionimage
            promotion_image_serializer = PromotionImageSerializer(promotion_image)
            image_url = request.build_absolute_uri(promotion_image_serializer.data["image"])
            return image_url
        except PromotionImage.DoesNotExist:
            return None

    class Meta:
        model = Promotion
        fields = ['id', 'title', 'description', 'insta_url', 'image']

class PromotionBannerSerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()

    def get_banner(self, instance):
        request = self.context.get('request')
        try:
            promotion_banner_image = instance.promotionbannerimage
            promotion_banner_image_serializer = PromotionBannerImageSerializer(promotion_banner_image)
            image_url = request.build_absolute_uri(promotion_banner_image_serializer.data["image"])
            return image_url
        except PromotionBannerImage.DoesNotExist:
            return None
    class Meta:
        model = Promotion
        fields = ['id', 'insta_url', 'banner']