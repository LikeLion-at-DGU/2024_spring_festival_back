from django.contrib import admin
from .models import Booth, BoothLocationOperationTime, BoothLike, BoothImage, Comment

class BoothLocationOperationTimeInline(admin.TabularInline):
    model = BoothLocationOperationTime
    extra = 1

class BoothAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'operator', 'show_operation_times')
    list_filter = ('type', 'operator')
    search_fields = ('name', 'description', 'operator')
    inlines = [BoothLocationOperationTimeInline]

    def show_operation_times(self, obj):
        operation_times = obj.location_operation_times.all()
        if operation_times:
            return ', '.join([f"{time.date.strftime('%A')} {time.start_time.strftime('%H:%M')} ~ {time.end_time.strftime('%H:%M')}" for time in operation_times])
        else:
            return "운영 시간이 없습니다."

    show_operation_times.short_description = '운영 시간'

admin.site.register(Booth, BoothAdmin)
admin.site.register(BoothLike)
admin.site.register(BoothImage)
admin.site.register(Comment)

