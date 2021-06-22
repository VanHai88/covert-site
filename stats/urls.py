from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.user_stats, name='user-stats'),
    path('users/ajax', views.ajax_user_stats, name='ajax-user-stats'),
]
