from django.urls import path
from .views import *

urlpatterns = [
    path('all/', all_videos, name='all-videos'),
]