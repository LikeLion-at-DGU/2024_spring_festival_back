from django.contrib import admin
from .models import *
# Register your models here.
class NotificationImageInline(admin.TabularInline):
    model = NotificationImage
    extra = 1

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    inlines = [NotificationImageInline]

admin.site.register(Notification, NotificationAdmin)

admin.site.register(NotificationImage)