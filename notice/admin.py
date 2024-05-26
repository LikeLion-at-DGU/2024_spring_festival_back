from django.contrib import admin
from .models import *
# Register your models here.
class NotificationImageInline(admin.TabularInline):
    model = NotificationImage
    extra = 1

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # 리스트 페이지에 제목과 생성 시간을 표시
    list_filter = ('created_at',)  # 생성 날짜로 필터링할 수 있도록 설정
    search_fields = ('title', 'description')  # 제목과 설명에서 검색할 수 있도록 설정
    inlines = [NotificationImageInline]

admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationImage)