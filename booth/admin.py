from django.contrib import admin
from .models import Booth, BoothOperationTime, BoothLike, BoothImage, Comment

class BoothOperationTimeInline(admin.TabularInline):
    model = BoothOperationTime
    extra = 1

class BoothAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'operator', 'show_operation_times')
    list_filter = ('type', 'location', 'operator')
    search_fields = ('name', 'description', 'operator')
    inlines = [BoothOperationTimeInline]

    def show_operation_times(self, obj):
        operation_times = obj.operation_times.all()
        if operation_times:
            return ', '.join([f"{time.date.strftime('%A')} {time.start_time.strftime('%H:%M')} ~ {time.end_time.strftime('%H:%M')}" for time in operation_times])
        else:
            return "운영 시간이 없습니다."

    show_operation_times.short_description = '운영 시간'

admin.site.register(Booth, BoothAdmin)
admin.site.register(BoothLike)
admin.site.register(BoothImage)
admin.site.register(Comment)

