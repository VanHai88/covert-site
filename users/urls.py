from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('profile/', profile, name='user-profile'),
    path('course-attendance/', course_attendance, name='user-courses'),
    path('complete/', signup_complete, name='signup-complete'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
]
