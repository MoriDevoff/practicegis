from django.contrib import admin
from .models import Landmark, SoloGame

@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

@admin.register(SoloGame)
class SoloGameAdmin(admin.ModelAdmin):
    list_display = ('player', 'landmark', 'score', 'created_at')
    list_filter = ('player', 'created_at')
    search_fields = ('player__username', 'landmark__name')
    ordering = ('-created_at',)