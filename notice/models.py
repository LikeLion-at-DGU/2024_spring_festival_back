from django.db import models
from core.models import BaseImage

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    insta_url = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class NotificationImage(BaseImage):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)