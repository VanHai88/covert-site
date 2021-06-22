from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_news, name='all-news'),
    path('view/<str:uuid>/', views.view_news, name='view-news'),
]
