from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^image_upload/$', image_upload, name='froala_editor_image_upload'),
    url(r'^file_upload/$', file_upload, name='froala_editor_file_upload'),
]
