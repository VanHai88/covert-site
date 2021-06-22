from django.urls import path

from .views import (
    users_list,
    all_courses,
)

urlpatterns = [
    path('users/', users_list, name='users-courses'),
    path('all/', all_courses, name='all-courses'),
]
