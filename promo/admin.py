from django.contrib import admin
from .models import *
# Register your models here.
class PromotionImageInline(admin.TabularInline):
    model = PromotionImage
    extra = 1

class PromotionBannerImageInline(admin.TabularInline):
    model = PromotionBannerImage
    extra = 1

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'description')
    inlines = [PromotionImageInline, PromotionBannerImageInline]

admin.site.register(Promotion, PromotionAdmin)
admin.site.register(PromotionImage)
admin.site.register(PromotionBannerImage)