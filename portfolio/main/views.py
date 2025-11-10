from django.shortcuts import render
from .models import Experience, Achievement, Profile


def home(request):
    experiences = Experience.objects.all().order_by('-start_date')
    achievements = Achievement.objects.all().order_by('-date')
    licenses = achievements.filter(category='license')
    competitions = achievements.filter(category='competition')
    profile = Profile.objects.first()
    context = {
        'experiences': experiences,
        'achievements': achievements,
        'licenses': licenses,
        'competitions': competitions,
        'profile': profile,
    }
    return render(request, "main/index.html", context)
