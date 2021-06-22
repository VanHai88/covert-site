from django.urls import path
from .views import *

urlpatterns = [
    path('ajax/create-post/', ajax_create_post, name='ajax-create-post'),
    path('ajax/delete-post/', ajax_delete_post, name='ajax-delete-post'),
    path('main/', main_feed.as_view(), name='main-feed'),
]