from django.contrib import admin
from .models import Experience, Achievement, Profile, Testimonial, ContactMessage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('tiktok_url',)

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


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'focus_area', 'rating', 'created_at')
    list_filter = ('rating', 'focus_area', 'created_at')
    search_fields = ('name', 'organization', 'focus_area', 'quote')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')
