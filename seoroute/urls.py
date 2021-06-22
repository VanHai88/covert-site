from django.urls import path
from .views import *

urlpatterns = [
    path('', seo_redirect),
    path('<path:resource>', seo_redirect)
]