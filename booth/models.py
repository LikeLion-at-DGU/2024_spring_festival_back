from django.db import models
from core.models import *
from django.core.validators import RegexValidator
from django.utils import timezone
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
    insta_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class BoothLocationOperationTime(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='location_operation_times')
    location = models.CharField(choices=LOCATION_CHOICES, max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('booth', 'date')

    def __str__(self):
        return f'{self.booth.name} on {self.date} from {self.start_time} to {self.end_time}'

class BoothLike(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='likes')
    key = models.CharField(
        max_length=10,
        blank=True,
        editable=False
    )
    fingerprint = models.CharField(max_length=64, default="None")  # SHA-256 해시 길이
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.booth}/{self.key}'

class BoothImage(BaseImage):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='boothimages')
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

class Comment(models.Model):
    booth=models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='comments')
    content=models.TextField()
    password = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex='^\d{4}$', message='Error : Password must be a 4-digit number')]
    )
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.booth}/{self.content[:20]}'
