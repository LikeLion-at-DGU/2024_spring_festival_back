from django.contrib import admin
from .models import *
# Register your models here.
class ArtistImageInline(admin.TabularInline):
    model = ArtistImage
    extra = 1

class MusicImageInline(admin.TabularInline):
    model = MusicImage
    extra = 1

class MusicInline(admin.TabularInline):
    model = Music
    extra = 1

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name',)
    inlines = [ArtistImageInline, MusicInline]

class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'ytb_url')
    search_fields = ('title', 'artist__name')
    inlines = [MusicImageInline]

admin.site.register(Performance)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(ArtistImage)
admin.site.register(MusicImage)