from django.db import models
from core.models import *
# Create your models here.

TYPE_CHOICES=(
        ('부스','부스'),
        ('푸드트럭','푸드트럭'),
        ('플리마켓','플리마켓'),
    )

LOCATION_CHOICES=(
        ('사회과학관','사회과학관'),
        ('혜화관','혜화관'),
        ('팔정도','팔정도'),
        ('원흥관','원흥관'),
        ('만해광장','만해광장'),
        ('학생회관','학생회관'),
        ('학림관','학림관'),
    )

class Booth(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=False, null=False, max_length=30)
    description = models.CharField(blank=True, null=False, max_length=300)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    operator = models.CharField(max_length=10)
    location = models.CharField(choices=LOCATION_CHOICES, max_length=10)
    latitude = models.FloatField()
    longtude = models.FloatField()
    insta_url = models.URLField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

# 부스 좋아요
class BoothLike(models.Model):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='likes')
    key=models.CharField(
        max_length=10,
        blank=True,
        editable=False
    )
    
    def __str__(self):
        return f'{self.booth}/{self.key}'

class BoothImage(BaseImage):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='boothimages')
    image = models.ImageField(upload_to=booth_image_upload_path, blank=True, null=True)