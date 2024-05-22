from django.contrib import admin
from .models import Booth, BoothImage, BoothLike, Comment
# Register your models here.
admin.site.register(Booth)
admin.site.register(BoothImage)
admin.site.register(BoothLike)
admin.site.register(Comment)