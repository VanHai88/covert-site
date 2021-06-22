from django.shortcuts import render
from django.views.decorators.http import require_POST

from collections import defaultdict
from datetime import date, timedelta

# Create your views here.
from .models import VideoPage

def all_videos(request):
    videos = VideoPage.objects.all()

    template = "all_videos.html"
    template_vars = {'videos':videos}
    return render(request, template, template_vars)
