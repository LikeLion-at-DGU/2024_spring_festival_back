from django.db import models
from core.models import BaseImage

# Create your models here.
class Performance(models.Model):
    operator = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    date = models.DateField()
    
    def __str__(self):
        return self.operator
    
class Artist(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name

class Music(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    ytb_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.title
    
class ArtistImage(BaseImage):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

class MusicImage(BaseImage):
    music = models.OneToOneField(Music, on_delete=models.CASCADE)
