from django.db import models
from core.models import BaseImage

# Create your models here.
class Promotion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    insta_url = models.URLField(max_length=200, blank=True)
    
    def __str__(self):
        return self.title
    
class PromotionImage(BaseImage):
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)

class PromotionBannerImage(BaseImage):
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE)