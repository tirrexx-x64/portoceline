from django.contrib import admin
from .models import Experience, Achievement

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'role', 'organization', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'organization')
    search_fields = ('title', 'role', 'organization')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'date')
    list_filter = ('organization', 'date')
    search_fields = ('title', 'organization')
