from django.db import models

# Create your models here.

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class BaseImage(models.Model):
    image=models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    class Meta:
        abstract = True